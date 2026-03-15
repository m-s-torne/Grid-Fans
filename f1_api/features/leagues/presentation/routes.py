"""League presentation layer - HTTP routes and endpoints"""
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from f1_api.dependencies import get_db_session
from f1_api.dependencies.auth import get_current_user
from f1_api.features.user.domain.models import Users
from f1_api.features.market.application.use_cases import (
    InitializeLeagueOwnershipUseCase,
    InitializeUserTeamUseCase,
)
from f1_api.features.market.infrastructure.persistence.ownership_repository import OwnershipRepository
from f1_api.features.market.infrastructure.persistence.transaction_repository import TransactionRepository
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
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
from .team_routes import router as team_router
from .market_routes import router as market_router


router = APIRouter(prefix="/leagues", dependencies=[Depends(get_current_user)])
router.include_router(team_router)
router.include_router(market_router)

CURRENT_SEASON = 2025  # TODO: drive from config / DB


@router.post("/", response_model=LeagueResponseDTO)
def create_league(
    league: LeagueCreateDTO,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Create a new league and automatically add the creator as admin"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = CreateLeagueService(
        league_repo, user_repo, user_link_repo, session,
        initialize_ownership=InitializeLeagueOwnershipUseCase(
            ownership_repo=OwnershipRepository(session),
            drivers_repo=DriversRepository(session, CURRENT_SEASON),
        ),
        initialize_user_team=InitializeUserTeamUseCase(
            ownership_repo=OwnershipRepository(session),
            transactions_repo=TransactionRepository(session),
            user_teams_repo=UserTeamsRepositoryImpl(session),
            drivers_repo=DriversRepository(session, CURRENT_SEASON),
            session=session,
        ),
    )
    return service.execute(current_user.supabase_user_id, league)


@router.post("/join/")
def join_league(
    league_join: LeagueJoinDTO,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Join a league using join code"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = JoinLeagueService(
        league_repo, user_repo, user_link_repo, session,
        initialize_user_team=InitializeUserTeamUseCase(
            ownership_repo=OwnershipRepository(session),
            transactions_repo=TransactionRepository(session),
            user_teams_repo=UserTeamsRepositoryImpl(session),
            drivers_repo=DriversRepository(session, CURRENT_SEASON),
            session=session,
        ),
    )
    return service.execute(current_user.supabase_user_id, league_join)


@router.get("/user/me", response_model=List[LeagueListItemDTO])
def get_user_leagues(
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Get all leagues where the current user is a participant"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = GetUserLeaguesService(league_repo, user_repo, user_link_repo)
    return service.execute(current_user.supabase_user_id)


@router.get("/{league_id}", response_model=LeagueResponseDTO)
def get_league_by_id(
    league_id: int,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Get details of a specific league by ID - only for league participants"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    
    # Execute use case
    service = GetLeagueDetailsService(league_repo, user_repo, user_link_repo)
    return service.execute(league_id, current_user.supabase_user_id)


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
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Remove current user from a league and delete their team"""
    # Construct dependencies
    league_repo = LeagueRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    user_link_repo = UserLeagueLinkRepositoryImpl(session)
    user_teams_repo = UserTeamsRepositoryImpl(session)
    
    # Execute use case
    service = LeaveLeagueService(league_repo, user_repo, user_link_repo, user_teams_repo)
    result = service.execute(league_id, current_user.supabase_user_id)
    session.commit()
    return result
