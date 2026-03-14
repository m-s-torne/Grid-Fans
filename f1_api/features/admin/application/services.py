"""Admin application services"""
import logging
from datetime import datetime
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import Seasons, Events, Sessions
from f1_api.features.teams.domain.models import Teams
from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.admin.domain.interfaces import (
    IGetEventData, IGetSessionData, IGetSessionResults, IGetTeamData,
    IGetDriverData, IGetAllDriverTeamLinks, IReconcileDriverTeamLinks,
)

logger = logging.getLogger(__name__)


class UpdateSeasonService:
    """
    Service for updating all season data in the database.
    
    Orchestrates the database update process for events, sessions, teams,
    drivers, driver-team links, and session results.
    """
    
    def __init__(
        self,
        engine,
        get_event_data: IGetEventData | None = None,
        get_session_data: IGetSessionData | None = None,
        get_session_results: IGetSessionResults | None = None,
        get_team_data: IGetTeamData | None = None,
        get_driver_data: IGetDriverData | None = None,
        get_all_driver_team_links: IGetAllDriverTeamLinks | None = None,
        reconcile_driver_team_links: IReconcileDriverTeamLinks | None = None,
        driver_repo_cls=None,
        team_repo_cls=None,
        link_repo_cls=None,
        season_context_cls=None,
    ):
        """
        Initialize service with database engine and injected infrastructure dependencies.

        Args:
            engine: SQLAlchemy engine for database operations
            get_event_data: Callable to load event data (injected from routes)
            get_session_data: Callable to load session data (injected from routes)
            get_session_results: Callable to load session results (injected from routes)
            get_team_data: Callable to load team data (injected from routes)
            get_driver_data: Callable to load driver data (injected from routes)
            get_all_driver_team_links: Callable to load driver-team links (injected from routes)
            reconcile_driver_team_links: Callable to reconcile missing links (injected from routes)
            driver_repo_cls: DriversRepository class (injected from routes)
            team_repo_cls: TeamsRepository class (injected from routes)
            link_repo_cls: DriverTeamLinkRepository class (injected from routes)
            season_context_cls: SeasonContextController class (injected from routes)
        """
        self.engine = engine
        self._get_event_data = get_event_data
        self._get_session_data = get_session_data
        self._get_session_results = get_session_results
        self._get_team_data = get_team_data
        self._get_driver_data = get_driver_data
        self._get_all_driver_team_links = get_all_driver_team_links
        self._reconcile_driver_team_links = reconcile_driver_team_links
        self._driver_repo_cls = driver_repo_cls
        self._team_repo_cls = team_repo_cls
        self._link_repo_cls = link_repo_cls
        self._season_context_cls = season_context_cls
    
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
        assert self._get_event_data is not None, "get_event_data dependency not injected"
        assert self._get_session_data is not None, "get_session_data dependency not injected"
        assert self._get_session_results is not None, "get_session_results dependency not injected"
        assert self._get_team_data is not None, "get_team_data dependency not injected"
        assert self._get_driver_data is not None, "get_driver_data dependency not injected"
        assert self._get_all_driver_team_links is not None, "get_all_driver_team_links dependency not injected"
        assert self._reconcile_driver_team_links is not None, "reconcile_driver_team_links dependency not injected"
        assert self._driver_repo_cls is not None, "driver_repo_cls dependency not injected"
        assert self._team_repo_cls is not None, "team_repo_cls dependency not injected"
        assert self._link_repo_cls is not None, "link_repo_cls dependency not injected"
        assert self._season_context_cls is not None, "season_context_cls dependency not injected"
        try:
            year = datetime.now().year
            with Session(self.engine) as session:
                season_exists = session.exec(select(Seasons).where(Seasons.year == year)).first()
                if not season_exists:
                    session.add(Seasons(year=year))
                    session.commit()

                events: list[Events] = self._get_event_data(session, year)
                sessions: list[Sessions] = self._get_session_data(session, year)
                teams: list[Teams] = self._get_team_data(session)

                session.add_all([*events, *sessions, *teams])

                # Construct repos from injected classes — session is available here
                driver_repo = self._driver_repo_cls(session, year)
                team_repo = self._team_repo_cls(session)
                link_repo = self._link_repo_cls(session)
                season_context = self._season_context_cls(session)

                drivers: list[Drivers] = self._get_driver_data(session, driver_repo, season_context)
                
                session.add_all(drivers)
                session.commit()

                all_driver_team_links = self._get_all_driver_team_links(
                    year, driver_repo, team_repo, link_repo, season_context
                )
                session.add_all(all_driver_team_links)
                session.commit()
                
                # Reconcile missing DriverTeamLinks
                missing_links = await self._reconcile_driver_team_links(
                    session, year, driver_repo, team_repo, link_repo, season_context
                )
                if missing_links:
                    logger.info(f"Reconciliation: adding {len(missing_links)} missing DriverTeamLinks")
                    session.add_all(missing_links)
                    session.commit()

                all_session_results = self._get_session_results(year, session)
                session.add_all(all_session_results)
                session.commit()
                session.close()
                
            return {"status": "updated"}
            
        except Exception as e:
            logger.warning(f'Season update service interrupted: {e}')
            raise
