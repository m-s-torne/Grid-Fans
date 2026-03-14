"""Infrastructure wrapper: fetches driver data using the DriversController application service."""
from sqlmodel import Session
from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.core.f1_data.domain.interfaces import ISeasonContext
from f1_api.core.f1_data.application.services import DriversController


def get_driver_data(
    session: Session,
    driver_repo: IDriversRepository,
    season_context: ISeasonContext,
) -> list[Drivers]:
    drivers_controller = DriversController(session, repository=driver_repo, season_context=season_context)
    return drivers_controller.get_driver_data()
