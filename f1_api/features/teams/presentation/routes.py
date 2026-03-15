"""Teams presentation - FastAPI routes"""
from fastapi import APIRouter, Depends
from sqlmodel import Session
from f1_api.dependencies import get_db_session
from f1_api.dependencies.auth import get_current_user
from f1_api.features.teams.infrastructure.repositories import TeamsRepository
from f1_api.features.teams.application.services import GetTeamsWithStatsService

router = APIRouter(prefix="/teams", dependencies=[Depends(get_current_user)])


@router.get("/")
def get_teams(session: Session = Depends(get_db_session)):
    """Get all teams for the current season with accumulated points"""
    teams_repo = TeamsRepository(session)
    service = GetTeamsWithStatsService(teams_repo)
    return service.execute()
