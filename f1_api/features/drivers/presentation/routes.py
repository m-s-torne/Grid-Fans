"""Drivers presentation - FastAPI routes"""
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlmodel import Session
from f1_api.dependencies import get_db_session
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.drivers.application.services import GetDriversService

router = APIRouter(prefix="/drivers", tags=["Drivers"])


@router.get("/")
def get_drivers(session: Session = Depends(get_db_session)):
    """Get all drivers sorted by championship points up to the last round"""
    drivers_repo = DriversRepository(session, datetime.now().year)
    service = GetDriversService(drivers_repo, session)
    return service.execute()
