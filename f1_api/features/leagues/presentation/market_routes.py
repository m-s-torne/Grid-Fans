"""League market routes — driver purchase and sale operations within a league"""
import traceback
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from f1_api.dependencies import get_db_session
from f1_api.features.user.domain.models import Users
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl
from f1_api.features.user_teams.domain.models import UserTeams
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.market.infrastructure.persistence.ownership_repository import OwnershipRepository
from f1_api.features.market.infrastructure.persistence.transaction_repository import TransactionRepository
from f1_api.features.market.infrastructure.persistence.buyout_repository import BuyoutRepository
from f1_api.features.market.application.use_cases import (
    GetFreeDriversUseCase,
    GetDriversForSaleUseCase,
    GetUserDriversUseCase,
    PurchaseDriverUseCase,
    PurchaseFromUserUseCase,
    SellToMarketUseCase,
    ListDriverForSaleUseCase,
    UnlistDriverUseCase,
    BuyoutClauseUseCase,
)
from f1_api.features.market.application.dtos.requests import (
    PurchaseDriverRequest,
    PurchaseFromUserRequest,
    SellToMarketRequest,
    ListDriverForSaleRequest,
    UnlistDriverRequest,
    BuyoutClauseRequest,
)
from f1_api.features.market.application.dtos.responses import (
    DriverOwnershipResponse,
    PurchaseResultResponse,
)
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl

router = APIRouter(tags=["leagues"])

CURRENT_SEASON = 2025  # TODO: drive from config / DB


# ============================================================================
# MARKET GET ENDPOINTS
# ============================================================================

@router.get("/{league_id}/market/free-drivers")
def get_free_drivers_in_league(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all free agent drivers available in the market"""
    try:
        ownership_repo = OwnershipRepository(session)
        drivers_repo = DriversRepository(session, CURRENT_SEASON)
        use_case = GetFreeDriversUseCase(ownership_repo, drivers_repo)
        result = use_case.execute(league_id)
        print(f"[DDD ROUTER] get_free_drivers({league_id}) returned {len(result)} drivers")
        if result:
            print(f"[DDD ROUTER] First driver: {result[0].get('full_name', 'N/A')}")
        return result
    except Exception as e:
        print(f"[DDD ROUTER ERROR] get_free_drivers failed: {e}")
        print(traceback.format_exc())
        raise


@router.get("/{league_id}/market/for-sale")
def get_drivers_for_sale_in_league(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all drivers listed for sale by other users"""
    ownership_repo = OwnershipRepository(session)
    drivers_repo = DriversRepository(session, CURRENT_SEASON)
    users_repo = UserRepositoryImpl(session)
    use_case = GetDriversForSaleUseCase(ownership_repo, drivers_repo, users_repo)
    result = use_case.execute(league_id)
    print(f"[DDD ROUTER] get_drivers_for_sale({league_id}) returned {len(result)} drivers")
    if result:
        print(f"[DDD ROUTER] First driver: {result[0].get('full_name', 'N/A')}")
    return result


@router.get("/{league_id}/market/user-drivers/{user_id}")
def get_user_drivers_in_league(
    league_id: int,
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Get all drivers owned by a specific user"""
    print(f"[DDD ROUTER] get_user_drivers called with user_id={user_id}, league_id={league_id}")
    try:
        internal_user_id = int(user_id)
        print(f"[DDD ROUTER] Parsed as int: internal_user_id={internal_user_id}")
    except ValueError as exc:
        print(f"[DDD ROUTER] Not an int, looking up UUID: {user_id}")
        user = session.exec(
            select(Users).where(Users.supabase_user_id == user_id)
        ).first()
        if not user:
            print(f"[DDD ROUTER] User not found for UUID: {user_id}")
            raise HTTPException(
                status_code=404,
                detail=f"User not found with UUID: {user_id}"
            ) from exc
        internal_user_id = user.id
        print(f"[DDD ROUTER] Found user: internal_user_id={internal_user_id}")

    ownership_repo = OwnershipRepository(session)
    drivers_repo = DriversRepository(session, CURRENT_SEASON)
    use_case = GetUserDriversUseCase(ownership_repo, drivers_repo)
    result = use_case.execute(internal_user_id, league_id)
    print(f"[DDD ROUTER] get_user_drivers({internal_user_id}, {league_id}) returned {len(result)} drivers")
    if result:
        print(f"[DDD ROUTER] First owned driver: {result[0].get('full_name', 'N/A')}")
    else:
        print(f"[DDD ROUTER] WARNING: No drivers found for user_id={internal_user_id} in league_id={league_id}")
    return result


# ============================================================================
# MARKET POST ENDPOINTS
# ============================================================================

@router.post("/{league_id}/market/buy-from-market/{driver_id}")
def buy_driver_from_market_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"buyer_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Buy a free agent driver from the market"""
    try:
        team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["buyer_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        current_budget = float(team.budget_remaining)
        ddd_request = PurchaseDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["buyer_user_id"]
        )
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = PurchaseDriverUseCase(ownership_repo, transaction_repo, user_teams_repo)
        success, result = use_case.execute(ddd_request, current_budget)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Purchase failed"))

        assert isinstance(result, PurchaseResultResponse)
        session.commit()
        return {
            "success": True,
            "driver_id": driver_id,
            "price": result.ownership.acquisition_price,
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "new_budget": result.budget_remaining
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{league_id}/market/buy-from-user/{driver_id}")
def buy_driver_from_user_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"buyer_user_id": int, "seller_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Buy a driver listed for sale from another user"""
    try:
        buyer_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["buyer_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not buyer_team:
            raise HTTPException(status_code=404, detail="Buyer team not found")

        seller_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["seller_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not seller_team:
            raise HTTPException(status_code=404, detail="Seller team not found")

        current_budget = float(buyer_team.budget_remaining)
        ddd_request = PurchaseFromUserRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=request["buyer_user_id"],
            seller_id=request["seller_user_id"]
        )
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = PurchaseFromUserUseCase(ownership_repo, transaction_repo, user_teams_repo)
        success, result = use_case.execute(ddd_request, current_budget)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Purchase failed"))

        assert isinstance(result, PurchaseResultResponse)
        session.commit()
        session.refresh(seller_team)
        return {
            "success": True,
            "driver_id": driver_id,
            "price": result.transaction.transaction_price,
            "seller_id": request["seller_user_id"],
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "buyer_new_budget": result.budget_remaining,
            "seller_new_budget": float(seller_team.budget_remaining)
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{league_id}/market/sell-to-market/{driver_id}")
def sell_driver_to_market_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"seller_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Quick sell a driver back to the market"""
    try:
        team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["seller_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")

        ddd_request = SellToMarketRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["seller_user_id"]
        )
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = SellToMarketUseCase(ownership_repo, transaction_repo, user_teams_repo)
        success, result = use_case.execute(ddd_request)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Sale failed"))

        session.commit()
        session.refresh(team)
        return {
            "success": True,
            "driver_id": driver_id,
            "refund": 0,
            "new_budget": float(team.budget_remaining)
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{league_id}/market/list-for-sale/{driver_id}")
def list_driver_for_sale_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"owner_user_id": int, "asking_price": float | None}
    session: Session = Depends(get_db_session)
):
    """List a driver for sale"""
    try:
        ddd_request = ListDriverForSaleRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["owner_user_id"],
            asking_price=request.get("asking_price")
        )
        ownership_repo = OwnershipRepository(session)
        use_case = ListDriverForSaleUseCase(ownership_repo)
        success, result = use_case.execute(ddd_request)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Listing failed"))

        assert isinstance(result, DriverOwnershipResponse)
        session.commit()
        return {
            "success": True,
            "driver_id": driver_id,
            "asking_price": result.asking_price,
            "is_listed": True
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/{league_id}/market/list-for-sale/{driver_id}")
def unlist_driver_from_sale_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"owner_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Remove a driver from sale listings"""
    try:
        ddd_request = UnlistDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["owner_user_id"]
        )
        ownership_repo = OwnershipRepository(session)
        use_case = UnlistDriverUseCase(ownership_repo)
        success, result = use_case.execute(ddd_request)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Unlisting failed"))

        session.commit()
        return {
            "success": True,
            "driver_id": driver_id,
            "is_listed": False
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/{league_id}/market/buyout-clause/{driver_id}")
def execute_buyout_clause_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"buyer_user_id": int, "victim_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Execute a buyout clause on another user's driver"""
    try:
        buyer_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["buyer_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not buyer_team:
            raise HTTPException(status_code=404, detail="Buyer team not found")

        victim_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["victim_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        if not victim_team:
            raise HTTPException(status_code=404, detail="Victim team not found")

        current_budget = float(buyer_team.budget_remaining)
        ddd_request = BuyoutClauseRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=request["buyer_user_id"],
            victim_id=request["victim_user_id"],
            season_year=datetime.now().year
        )
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        buyout_repo = BuyoutRepository(session)
        use_case = BuyoutClauseUseCase(ownership_repo, transaction_repo, buyout_repo)
        success, result = use_case.execute(ddd_request, current_budget)

        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Buyout failed"))

        assert isinstance(result, PurchaseResultResponse)
        session.commit()
        session.refresh(buyer_team)
        session.refresh(victim_team)
        return {
            "success": True,
            "driver_id": driver_id,
            "buyout_price": result.transaction.transaction_price,
            "buyer_new_budget": float(buyer_team.budget_remaining),
            "victim_new_budget": float(victim_team.budget_remaining),
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "replacement_info": None
        }
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e
