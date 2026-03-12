"""Admin presentation - FastAPI routes"""
from fastapi import APIRouter
from f1_api.config.sql_init import engine
from f1_api.features.admin.application.services import UpdateSeasonService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/season/")
async def update_season():
    """Update all data for the current season in the database"""
    service = UpdateSeasonService(engine)
    return await service.execute()
