"""
User Teams Presentation Layer - HTTP Routes
FastAPI endpoints for user teams management
"""
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from f1_api.dependencies.database import get_db_session
from f1_api.dependencies.auth import get_current_user
from f1_api.features.user.domain.models import Users

from ..application.dtos import UserTeamUpdateDTO, UserTeamResponseDTO, SwapReserveDriverDTO
from ..application.services import (
    CreateOrUpdateTeamService, 
    GetMyTeamService,
    SwapReserveDriverService
)
from ..infrastructure.repositories import UserTeamsRepositoryImpl

from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl
from f1_api.features.leagues.infrastructure.repositories import UserLeagueLinkRepositoryImpl

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user-teams", dependencies=[Depends(get_current_user)])


def get_user_teams_repository(session: Session = Depends(get_db_session)) -> UserTeamsRepositoryImpl:
    """Dependency injection for UserTeamsRepository"""
    return UserTeamsRepositoryImpl(session)


def get_user_repository(session: Session = Depends(get_db_session)) -> UserRepositoryImpl:
    """Dependency injection for UserRepository"""
    return UserRepositoryImpl(session)


def get_league_link_repository(session: Session = Depends(get_db_session)) -> UserLeagueLinkRepositoryImpl:
    """Dependency injection for UserLeagueLinkRepository"""
    return UserLeagueLinkRepositoryImpl(session)


@router.post("/leagues/{league_id}/teams", response_model=UserTeamResponseDTO)
def create_or_update_team(
    league_id: int,
    team_data: UserTeamUpdateDTO,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
    user_teams_repo: UserTeamsRepositoryImpl = Depends(get_user_teams_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
    league_link_repo: UserLeagueLinkRepositoryImpl = Depends(get_league_link_repository)
):
    """
    Create or update a user's team in a specific league
    
    - **league_id**: ID of the league for the team
    - **team_data**: Team configuration (name, drivers, constructor)
    
    Returns the created or updated team with calculated budget
    """
    try:
        service = CreateOrUpdateTeamService(
            session=session,
            user_teams_repo=user_teams_repo,
            user_repo=user_repo,
            league_link_repo=league_link_repo
        )
        
        result = service.execute(league_id, team_data, current_user.supabase_user_id)
        
        logger.info(f"User {current_user.supabase_user_id} created/updated team in league {league_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating/updating team: {e}", exc_info=True)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get("/leagues/{league_id}/teams/me", response_model=UserTeamResponseDTO | None)
def get_my_team(
    league_id: int,
    current_user: Users = Depends(get_current_user),
    user_teams_repo: UserTeamsRepositoryImpl = Depends(get_user_teams_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository)
):
    """
    Get the current user's team in a specific league
    
    - **league_id**: ID of the league
    
    Returns the user's team or None if no team exists
    """
    try:
        service = GetMyTeamService(
            user_teams_repo=user_teams_repo,
            user_repo=user_repo
        )
        
        result = service.execute(league_id, current_user.supabase_user_id)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting team: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.post("/leagues/{league_id}/teams/swap-reserve")
def swap_reserve_driver(
    league_id: int,
    request: SwapReserveDriverDTO,
    session: Session = Depends(get_db_session),
    user_teams_repo: UserTeamsRepositoryImpl = Depends(get_user_teams_repository)
):
    """
    Swap a main driver with the reserve driver
    
    - **league_id**: ID of the league
    - **request**: Swap request with user_id and driver_id
    
    The specified driver_id will become the reserve, and the current reserve will take its slot
    """
    try:
        service = SwapReserveDriverService(
            session=session,
            user_teams_repo=user_teams_repo
        )
        
        result = service.execute(
            user_id=request.user_id,
            driver_id=request.driver_id,
            league_id=league_id
        )
        
        logger.info(f"User {request.user_id} swapped reserve driver in league {league_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error swapping reserve driver: {e}", exc_info=True)
        session.rollback()
        raise HTTPException(status_code=500, detail="Internal server error") from e
