"""League presentation layer - HTTP routes and endpoints"""
import traceback
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from f1_api.dependencies import get_db_session
from f1_api.features.user.domain.models import Users
from f1_api.features.user_teams.application.services import GetMyTeamService, SwapReserveDriverService
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl
from f1_api.features.user_teams.domain.models import UserTeams
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.market.infrastructure.persistence.ownership_repository import OwnershipRepository
from f1_api.features.market.infrastructure.persistence.transaction_repository import TransactionRepository
from f1_api.features.market.infrastructure.persistence.buyout_repository import BuyoutRepository
from f1_api.features.market.application.use_cases import (
    InitializeLeagueOwnershipUseCase,
    InitializeUserTeamUseCase,
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
from ..application.dtos import (
    LeagueCreateDTO,
    LeagueResponseDTO,
    LeagueJoinDTO,
    LeagueListItemDTO
)
from ..application.services import (
    CreateLeagueService,
    JoinLeagueService,
    GetUserLeaguesService,
    GetLeagueDetailsService,
    GetLeagueParticipantsService,
    LeaveLeagueService
)
from ..infrastructure.repositories import (
    LeagueRepositoryImpl,
    UserLeagueLinkRepositoryImpl
)
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl


router = APIRouter(prefix="/leagues", tags=["leagues"])


@router.post("/", response_model=LeagueResponseDTO)
def create_league(
    league: LeagueCreateDTO,
    admin_user_id: str,
    session: Session = Depends(get_db_session)
):
    """Create a new league and automatically add the creator as admin"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = CreateLeagueService(
        league_repo, user_repo, user_link_repo, session,
        initialize_ownership=InitializeLeagueOwnershipUseCase(session),
        initialize_user_team=InitializeUserTeamUseCase(session),
    )
    return service.execute(admin_user_id, league)


@router.post("/join/")
def join_league(
    league_join: LeagueJoinDTO,
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Join a league using join code"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = JoinLeagueService(
        league_repo, user_repo, user_link_repo, session,
        initialize_user_team=InitializeUserTeamUseCase(session),
    )
    return service.execute(user_id, league_join)


@router.get("/user/{user_id}", response_model=List[LeagueListItemDTO])
def get_user_leagues(
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Get all leagues where the user is a participant"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = GetUserLeaguesService(league_repo, user_repo, user_link_repo)
    return service.execute(user_id)


@router.get("/{league_id}", response_model=LeagueResponseDTO)
def get_league_by_id(
    league_id: int,
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Get details of a specific league by ID - only for league participants"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = GetLeagueDetailsService(league_repo, user_repo, user_link_repo)
    return service.execute(league_id, user_id)


@router.get("/{league_id}/participants")
def get_league_participants(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all participants of a specific league"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = GetLeagueParticipantsService(league_repo, user_link_repo)
    result = service.execute(league_id)
    print(f"[DDD ROUTER] get_league_participants({league_id}) returned {result.get('total_participants', 0)} participants")
    if result.get("participants"):
        print(f"[DDD ROUTER] First participant: {result['participants'][0]}")
    else:
        print(f"[DDD ROUTER] WARNING: No participants found for league_id={league_id}")
    return result


@router.delete("/{league_id}/leave")
def leave_league(
    league_id: int,
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Remove user from a league and delete their team"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = LeaveLeagueService(league_repo, user_repo, user_link_repo, session)
    return service.execute(league_id, user_id)




@router.get("/{league_id}/teams/me")
def get_my_team_in_league(
    league_id: int,
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """Get the current user's team in a specific league"""
    user_teams_repo = UserTeamsRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    service = GetMyTeamService(user_teams_repo, user_repo)
    return service.execute(league_id, user_id)


@router.post("/{league_id}/teams/swap-reserve")
def swap_reserve_driver_in_league(
    league_id: int,
    request: dict,  # {"user_id": int, "driver_id": int}
    session: Session = Depends(get_db_session)
):
    """Swap a main driver with the reserve driver"""
    user_teams_repo = UserTeamsRepositoryImpl(session)
    service = SwapReserveDriverService(session, user_teams_repo)
    return service.execute(
        user_id=request["user_id"],
        driver_id=request["driver_id"],
        league_id=league_id
    )


# ============================================================================
# MARKET GET ENDPOINTS - Driver listings and availability (DDD Backend)
# ============================================================================

@router.get("/{league_id}/market/free-drivers")
def get_free_drivers_in_league(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all free agent drivers available in the market (uses DDD backend)"""
    try:
        # Constants
        CURRENT_SEASON = 2025
        
        # Construct repositories
        ownership_repo = OwnershipRepository(session)
        drivers_repo = DriversRepository(session, CURRENT_SEASON)
        
        # Execute use case
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
    """Get all drivers listed for sale by other users (uses DDD backend)"""
    # Constants
    CURRENT_SEASON = 2025
    
    # Construct repositories
    ownership_repo = OwnershipRepository(session)
    drivers_repo = DriversRepository(session, CURRENT_SEASON)
    users_repo = UserRepositoryImpl(session)
    
    # Execute use case
    use_case = GetDriversForSaleUseCase(ownership_repo, drivers_repo, users_repo)
    result = use_case.execute(league_id)
    
    print(f"[DDD ROUTER] get_drivers_for_sale({league_id}) returned {len(result)} drivers")
    if result:
        print(f"[DDD ROUTER] First driver: {result[0].get('full_name', 'N/A')}")
    return result


@router.get("/{league_id}/market/user-drivers/{user_id}")
def get_user_drivers_in_league(
    league_id: int,
    user_id: str,  # Accept both UUID and internal ID
    session: Session = Depends(get_db_session)
):
    """Get all drivers owned by a specific user (uses DDD backend)"""
    # Constants
    CURRENT_SEASON = 2025
    
    print(f"[DDD ROUTER] get_user_drivers called with user_id={user_id}, league_id={league_id}")
    
    # Try to convert UUID to internal user_id
    try:
        # First, try to parse as int (backward compatibility)
        internal_user_id = int(user_id)
        print(f"[DDD ROUTER] Parsed as int: internal_user_id={internal_user_id}")
    except ValueError as exc:
        # It's a UUID string, look up the internal ID
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
    
    # Construct repositories
    ownership_repo = OwnershipRepository(session)
    drivers_repo = DriversRepository(session, CURRENT_SEASON)
    
    # Execute use case
    use_case = GetUserDriversUseCase(ownership_repo, drivers_repo)
    result = use_case.execute(internal_user_id, league_id)
    
    print(f"[DDD ROUTER] get_user_drivers({internal_user_id}, {league_id}) returned {len(result)} drivers")
    if result:
        print(f"[DDD ROUTER] First owned driver: {result[0].get('full_name', 'N/A')}")
    else:
        print(f"[DDD ROUTER] WARNING: No drivers found for user_id={internal_user_id} in league_id={league_id}")
    return result


# ============================================================================
# MARKET POST ENDPOINTS - Driver purchase and sale operations (DDD Backend)
# ============================================================================

@router.post("/{league_id}/market/buy-from-market/{driver_id}")
def buy_driver_from_market_in_league(
    league_id: int,
    driver_id: int,
    request: dict,  # {"buyer_user_id": int}
    session: Session = Depends(get_db_session)
):
    """Buy a free agent driver from the market (uses DDD backend)"""
    try:
        # Get user's current budget
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
        
        # Create DDD request
        ddd_request = PurchaseDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["buyer_user_id"]
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = PurchaseDriverUseCase(ownership_repo, transaction_repo, user_teams_repo)
        
        success, result = use_case.execute(ddd_request, current_budget)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Purchase failed"))
        
        session.commit()
        
        # Transform DDD response to legacy format
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "price": result.ownership.acquisition_price,
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "new_budget": result.budget_remaining
        }
        
        return legacy_response
        
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
    """Buy a driver listed for sale from another user (uses DDD backend)"""
    try:
        # Get buyer's current budget
        buyer_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["buyer_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        
        if not buyer_team:
            raise HTTPException(status_code=404, detail="Buyer team not found")
        
        # Get seller's current budget (for response)
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
        
        # Create DDD request
        ddd_request = PurchaseFromUserRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=request["buyer_user_id"],
            seller_id=request["seller_user_id"]
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = PurchaseFromUserUseCase(ownership_repo, transaction_repo, user_teams_repo)
        
        success, result = use_case.execute(ddd_request, current_budget)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Purchase failed"))
        
        session.commit()
        
        # Get updated seller budget
        session.refresh(seller_team)
        
        # Transform DDD response to legacy format
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "price": result.transaction.transaction_price,
            "seller_id": request["seller_user_id"],
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "buyer_new_budget": result.budget_remaining,
            "seller_new_budget": float(seller_team.budget_remaining)
        }
        
        return legacy_response
        
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
    """Quick sell a driver back to the market (uses DDD backend)"""
    try:
        # Get user's current team (for updated budget)
        team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["seller_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        # Create DDD request  
        ddd_request = SellToMarketRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["seller_user_id"]
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        user_teams_repo = UserTeamsRepositoryImpl(session)
        use_case = SellToMarketUseCase(ownership_repo, transaction_repo, user_teams_repo)
        
        success, result = use_case.execute(ddd_request)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Sale failed"))
        
        session.commit()
        
        # Get updated team budget
        session.refresh(team)
        
        # Transform DDD response to legacy format
        # SellToMarket releases driver (no refund in current implementation)
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "refund": 0,  # Released to market, no refund
            "new_budget": float(team.budget_remaining)
        }
        
        return legacy_response
        
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
    """List a driver for sale (uses DDD backend)"""
    try:
        # Create DDD request
        ddd_request = ListDriverForSaleRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["owner_user_id"],
            asking_price=request.get("asking_price")
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        use_case = ListDriverForSaleUseCase(ownership_repo)
        
        success, result = use_case.execute(ddd_request)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Listing failed"))
        
        session.commit()
        
        # Transform DDD response to legacy format
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "asking_price": result.asking_price,
            "is_listed": True
        }
        
        return legacy_response
        
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
    """Remove a driver from sale listings (uses DDD backend)"""
    try:
        # Create DDD request
        ddd_request = UnlistDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=request["owner_user_id"]
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        use_case = UnlistDriverUseCase(ownership_repo)
        
        success, result = use_case.execute(ddd_request)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Unlisting failed"))
        
        session.commit()
        
        # Transform DDD response to legacy format
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "is_listed": False
        }
        
        return legacy_response
        
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
    """Execute a buyout clause on another user's driver (uses DDD backend)"""
    try:
        # Get buyer's current budget
        buyer_team = session.exec(
            select(UserTeams).where(
                UserTeams.user_id == request["buyer_user_id"],
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        
        if not buyer_team:
            raise HTTPException(status_code=404, detail="Buyer team not found")
        
        # Get victim's team (for response)
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
        
        # Create DDD request (use current year as season_year)
        current_year = datetime.now().year
        
        ddd_request = BuyoutClauseRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=request["buyer_user_id"],
            victim_id=request["victim_user_id"],
            season_year=current_year
        )
        
        # Execute use case
        ownership_repo = OwnershipRepository(session)
        transaction_repo = TransactionRepository(session)
        buyout_repo = BuyoutRepository(session)
        use_case = BuyoutClauseUseCase(ownership_repo, transaction_repo, buyout_repo)
        
        success, result = use_case.execute(ddd_request, current_budget)
        
        if not success:
            error_dict = result.model_dump()
            raise HTTPException(status_code=400, detail=error_dict.get("error", "Buyout failed"))
        
        session.commit()
        
        # Get updated budgets
        session.refresh(buyer_team)
        session.refresh(victim_team)
        
        # Transform DDD response to legacy format
        legacy_response = {
            "success": True,
            "driver_id": driver_id,
            "buyout_price": result.transaction.transaction_price,
            "buyer_new_budget": float(buyer_team.budget_remaining),
            "victim_new_budget": float(victim_team.budget_remaining),
            "locked_until": result.ownership.locked_until.isoformat() if result.ownership.locked_until else None,
            "replacement_info": None  # Legacy field, DDD doesn't handle replacement
        }
        
        return legacy_response
        
    except HTTPException:
        session.rollback()
        raise
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e)) from e