"""League team routes — user team operations within a league"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from f1_api.dependencies import get_db_session
from f1_api.dependencies.auth import get_current_user
from f1_api.features.user.domain.models import Users
from f1_api.features.user_teams.application.services import GetMyTeamService, SwapReserveDriverService
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl

router = APIRouter(tags=["leagues"])


@router.get("/{league_id}/teams/me")
def get_my_team_in_league(
    league_id: int,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Get the current user's team in a specific league"""
    user_teams_repo = UserTeamsRepositoryImpl(session)
    user_repo = UserRepositoryImpl(session)
    service = GetMyTeamService(user_teams_repo, user_repo)
    return service.execute(league_id, current_user.supabase_user_id)


@router.post("/{league_id}/teams/swap-reserve")
def swap_reserve_driver_in_league(
    league_id: int,
    request: dict,  # {"driver_id": int}
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    """Swap a main driver with the reserve driver"""
    user_teams_repo = UserTeamsRepositoryImpl(session)
    service = SwapReserveDriverService(session, user_teams_repo)
    return service.execute(
        user_id=current_user.supabase_user_id,
        driver_id=request["driver_id"],
        league_id=league_id
    )
