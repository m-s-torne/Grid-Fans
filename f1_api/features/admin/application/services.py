"""Admin application services"""
import logging
from datetime import datetime
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import Seasons, Events, Sessions
from f1_api.features.teams.domain.models import Teams
from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.admin.infrastructure.data_ingestion import (
    get_session_results,
    get_team_data,
    get_event_data,
    get_session_data,
)
from f1_api.core.f1_data.application.services import get_driver_data
from f1_api.core.f1_data.application.driver_team_link_service import get_all_driver_team_links
from f1_api.core.f1_data.application.driver_team_link_reconciliation import reconcile_driver_team_links

logger = logging.getLogger(__name__)


class UpdateSeasonService:
    """
    Service for updating all season data in the database.
    
    Orchestrates the database update process for events, sessions, teams,
    drivers, driver-team links, and session results.
    """
    
    def __init__(self, engine):
        """
        Initialize service with database engine.
        
        Args:
            engine: SQLAlchemy engine for database operations
        """
        self.engine = engine
    
    async def execute(self) -> dict:
        """
        Update all data for the current season in the database.
        
        Creates or updates:
        - Season record
        - Events (race weekends)
        - Sessions (practice, qualifying, race, sprint)
        - Teams (constructors)
        - Drivers
        - Driver-team links
        - Session results
        
        Returns:
            dict with status message
        """
        try:
            year = datetime.now().year
            with Session(self.engine) as session:
                season_exists = session.exec(select(Seasons).where(Seasons.year == year)).first()
                if not season_exists:
                    session.add(Seasons(year=year))
                    session.commit()

                events: list[Events] = get_event_data(session, year)
                sessions: list[Sessions] = get_session_data(session, year)
                teams: list[Teams] = get_team_data(session)

                session.add_all([*events, *sessions, *teams])

                drivers: list[Drivers] = get_driver_data(session)
                
                session.add_all(drivers)
                session.commit()
                
                all_driver_team_links = get_all_driver_team_links(session, year)
                session.add_all(all_driver_team_links)
                session.commit()
                
                # Reconcile missing DriverTeamLinks
                missing_links = await reconcile_driver_team_links(session, year)
                if missing_links:
                    logger.info(f"Reconciliation: adding {len(missing_links)} missing DriverTeamLinks")
                    session.add_all(missing_links)
                    session.commit()

                all_session_results = get_session_results(year, session)
                session.add_all(all_session_results)
                session.commit()
                session.close()
                
            return {"status": "updated"}
            
        except Exception as e:
            logger.warning(f'Season update service interrupted: {e}')
            raise
