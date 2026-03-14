"""Admin presentation - FastAPI routes"""
from fastapi import APIRouter, Depends
from f1_api.dependencies.auth import get_admin_user
from f1_api.config.sql_init import engine
from f1_api.features.admin.application.services import UpdateSeasonService
from f1_api.features.admin.infrastructure.data_ingestion import (
    get_event_data,
    get_session_data,
    get_session_results,
    get_team_data,
)
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.teams.infrastructure.repositories import TeamsRepository
from f1_api.core.f1_data.infrastructure.persistence.driver_team_link_repository import DriverTeamLinkRepository
from f1_api.core.f1_data.infrastructure.season_context import SeasonContextController
from f1_api.core.f1_data.infrastructure.driver_data import get_driver_data
from f1_api.core.f1_data.infrastructure.driver_team_link_data import get_all_driver_team_links, reconcile_driver_team_links

router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(get_admin_user)])


@router.post("/season/")
async def update_season():
    """Update all data for the current season in the database"""
    service = UpdateSeasonService(
        engine,
        get_event_data=get_event_data,
        get_session_data=get_session_data,
        get_session_results=get_session_results,
        get_team_data=get_team_data,
        get_driver_data=get_driver_data,
        get_all_driver_team_links=get_all_driver_team_links,
        reconcile_driver_team_links=reconcile_driver_team_links,
        driver_repo_cls=DriversRepository,
        team_repo_cls=TeamsRepository,
        link_repo_cls=DriverTeamLinkRepository,
        season_context_cls=SeasonContextController,
    )
    return await service.execute()
