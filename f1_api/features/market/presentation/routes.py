"""Market presentation layer - API routes (DDD Architecture)"""
from dataclasses import asdict
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel

from f1_api.dependencies import get_db_session
from f1_api.dependencies.auth import get_current_user
from f1_api.features.market.application.dtos.requests import (
    PurchaseDriverRequest,
    PurchaseFromUserRequest,
    ListDriverForSaleRequest,
    UnlistDriverRequest,
    SellToMarketRequest,
    BuyoutClauseRequest,
    EmergencyAssignmentRequest
)
from f1_api.features.market.application.use_cases.purchase_driver import PurchaseDriverUseCase
from f1_api.features.market.application.use_cases.purchase_from_user import PurchaseFromUserUseCase
from f1_api.features.market.application.use_cases.list_driver_for_sale import ListDriverForSaleUseCase
from f1_api.features.market.application.use_cases.unlist_driver import UnlistDriverUseCase
from f1_api.features.market.application.use_cases.sell_to_market import SellToMarketUseCase
from f1_api.features.market.application.use_cases.buyout_clause import BuyoutClauseUseCase
from f1_api.features.market.application.use_cases.emergency_assignment import EmergencyAssignmentUseCase
from f1_api.features.market.application.use_cases.get_market_stats import GetMarketStatsUseCase
from f1_api.features.market.infrastructure.persistence.ownership_repository import OwnershipRepository
from f1_api.features.market.infrastructure.persistence.transaction_repository import TransactionRepository
from f1_api.features.market.infrastructure.persistence.buyout_repository import BuyoutRepository
from f1_api.features.user_teams.domain.models import UserTeams
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl

router = APIRouter(prefix="/market", dependencies=[Depends(get_current_user)])


# ============================================================================
#  HELPER FUNCTIONS
# ============================================================================

def _get_user_budget(session: Session, user_id: int, league_id: int) -> float:
    """Get user's current budget from their team."""
    team = session.exec(
        select(UserTeams).where(
            UserTeams.user_id == user_id,
            UserTeams.league_id == league_id,
            UserTeams.is_active == True
        )
    ).first()
    
    if not team:
        raise HTTPException(
            status_code=404,
            detail=f"Active team not found for user {user_id} in league {league_id}"
        )
    
    return float(team.budget_remaining)


# ============================================================================
# REQUEST BODY MODELS (for FastAPI path parameters)
# ============================================================================

class PurchaseRequestBody(BaseModel):
    """Body for purchase from free market"""
    user_id: int


class PurchaseFromUserBody(BaseModel):
    """Body for purchase from another user"""
    buyer_id: int
    seller_id: int


class ListForSaleBody(BaseModel):
    """Body for listing driver for sale"""
    user_id: int
    asking_price: float


class UnlistBody(BaseModel):
    """Body for unlisting driver"""
    user_id: int


class SellToMarketBody(BaseModel):
    """Body for selling to market"""
    user_id: int


class BuyoutBody(BaseModel):
    """Body for buyout clause"""
    buyer_id: int
    victim_id: int
    season_year: int


class EmergencyBody(BaseModel):
    """Body for emergency assignment"""
    user_id: int
    admin_id: int
    reason: str
    is_admin: bool = False


# ============================================================================
# MARKET QUERY ENDPOINTS (GET)
# ============================================================================

@router.get("/{league_id}/free-agents")
def get_free_agents(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all free agent drivers available in the market."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    use_case = GetMarketStatsUseCase(ownership_repo, transaction_repo)
    
    try:
        free_agents = use_case.get_free_agents(league_id)
        return [asdict(agent) for agent in free_agents]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{league_id}/listings")
def get_market_listings(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all drivers listed for sale by users."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    use_case = GetMarketStatsUseCase(ownership_repo, transaction_repo)
    
    try:
        listings = use_case.get_market_listings(league_id)
        return [asdict(listing) for listing in listings]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{league_id}/users/{user_id}/drivers")
def get_user_drivers(
    league_id: int,
    user_id: int,
    session: Session = Depends(get_db_session)
):
    """Get all drivers owned by a specific user."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    use_case = GetMarketStatsUseCase(ownership_repo, transaction_repo)
    
    try:
        drivers = use_case.get_user_drivers(user_id, league_id)
        return [asdict(driver) for driver in drivers]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{league_id}/stats")
def get_market_stats(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get market statistics and overview."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    use_case = GetMarketStatsUseCase(ownership_repo, transaction_repo)
    
    try:
        stats = use_case.get_market_stats(league_id)
        return stats
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.get("/{league_id}/transactions")
def get_transaction_history(
    league_id: int,
    session: Session = Depends(get_db_session)
):
    """Get transaction history for a league."""
    transaction_repo = TransactionRepository(session)
    
    try:
        transactions = transaction_repo.get_by_league(league_id)
        return [asdict(tx) for tx in transactions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


# ============================================================================
# MARKET TRANSACTION ENDPOINTS (POST)
# ============================================================================

@router.post("/{league_id}/purchase/free-agent/{driver_id}")
def purchase_free_agent(
    league_id: int,
    driver_id: int,
    body: PurchaseRequestBody,
    session: Session = Depends(get_db_session)
):
    """Purchase a free agent driver from the market."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    user_teams_repo = UserTeamsRepositoryImpl(session)
    use_case = PurchaseDriverUseCase(ownership_repo, transaction_repo, user_teams_repo)
    
    try:
        # Get current budget
        current_budget = _get_user_budget(session, body.user_id, league_id)
        
        # Build request DTO
        request = PurchaseDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=body.user_id
        )
        
        # Execute use case
        success, result = use_case.execute(request, current_budget)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.post("/{league_id}/purchase/from-user/{driver_id}")
def purchase_from_user(
    league_id: int,
    driver_id: int,
    body: PurchaseFromUserBody,
    session: Session = Depends(get_db_session)
):
    """Purchase a driver listed for sale from another user."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    user_teams_repo = UserTeamsRepositoryImpl(session)
    use_case = PurchaseFromUserUseCase(ownership_repo, transaction_repo, user_teams_repo)
    
    try:
        # Get current budget
        current_budget = _get_user_budget(session, body.buyer_id, league_id)
        
        # Build request DTO
        request = PurchaseFromUserRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=body.buyer_id,
            seller_id=body.seller_id
        )
        
        # Execute use case
        success, result = use_case.execute(request, current_budget)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.post("/{league_id}/list-for-sale/{driver_id}")
def list_driver_for_sale(
    league_id: int,
    driver_id: int,
    body: ListForSaleBody,
    session: Session = Depends(get_db_session)
):
    """List a driver for sale at a specified asking price."""
    ownership_repo = OwnershipRepository(session)
    use_case = ListDriverForSaleUseCase(ownership_repo)
    
    try:
        # Build request DTO
        request = ListDriverForSaleRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=body.user_id,
            asking_price=body.asking_price
        )
        
        # Execute use case
        success, result = use_case.execute(request)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.delete("/{league_id}/list-for-sale/{driver_id}")
def unlist_driver(
    league_id: int,
    driver_id: int,
    body: UnlistBody,
    session: Session = Depends(get_db_session)
):
    """Remove a driver from sale listings."""
    ownership_repo = OwnershipRepository(session)
    use_case = UnlistDriverUseCase(ownership_repo)
    
    try:
        # Build request DTO
        request = UnlistDriverRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=body.user_id
        )
        
        # Execute use case
        success, result = use_case.execute(request)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.post("/{league_id}/sell-to-market/{driver_id}")
def sell_to_market(
    league_id: int,
    driver_id: int,
    body: SellToMarketBody,
    session: Session = Depends(get_db_session)
):
    """Quick sell a driver back to the market (releases to free agency)."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    user_teams_repo = UserTeamsRepositoryImpl(session)
    use_case = SellToMarketUseCase(ownership_repo, transaction_repo, user_teams_repo)
    
    try:
        # Build request DTO
        request = SellToMarketRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=body.user_id
        )
        
        # Execute use case
        success, result = use_case.execute(request)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.post("/{league_id}/buyout/{driver_id}")
def execute_buyout_clause(
    league_id: int,
    driver_id: int,
    body: BuyoutBody,
    session: Session = Depends(get_db_session)
):
    """Execute a buyout clause to force-purchase a driver from another user."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    buyout_repo = BuyoutRepository(session)
    use_case = BuyoutClauseUseCase(ownership_repo, transaction_repo, buyout_repo)
    
    try:
        # Get current budget
        current_budget = _get_user_budget(session, body.buyer_id, league_id)
        
        # Build request DTO
        request = BuyoutClauseRequest(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=body.buyer_id,
            victim_id=body.victim_id,
            season_year=body.season_year
        )
        
        # Execute use case
        success, result = use_case.execute(request, current_budget)
        
        if not success:
            raise HTTPException(status_code=400, detail=result.model_dump())
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e


@router.post("/{league_id}/emergency-assignment/{driver_id}")
def emergency_assignment(
    league_id: int,
    driver_id: int,
    body: EmergencyBody,
    session: Session = Depends(get_db_session)
):
    """Admin-only: Assign a driver to a user in emergency situations."""
    ownership_repo = OwnershipRepository(session)
    transaction_repo = TransactionRepository(session)
    use_case = EmergencyAssignmentUseCase(ownership_repo, transaction_repo)
    
    try:
        # Build request DTO
        request = EmergencyAssignmentRequest(
            driver_id=driver_id,
            league_id=league_id,
            user_id=body.user_id,
            admin_id=body.admin_id,
            reason=body.reason,
            override_price=None
        )
        
        # Execute use case
        success, result = use_case.execute(request, body.is_admin)
        
        if not success:
            result_dict = result.model_dump()
            if result_dict.get('error_code') == "UNAUTHORIZED":
                raise HTTPException(status_code=403, detail=result_dict)
            raise HTTPException(status_code= 400, detail=result_dict)
        
        session.commit()
        return result.model_dump()
        
    except HTTPException:
        session.rollback()
        raise
    except ValueError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") from e
