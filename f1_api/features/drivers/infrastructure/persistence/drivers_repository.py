"""Drivers repository - read-only queries for driver data"""
from typing import Dict
from sqlmodel import Session, select, func
from f1_api.features.drivers.domain.models import Drivers, DriverTeamLink
from f1_api.features.teams.domain.models import Teams
from f1_api.core.f1_data.domain.models import SessionResult, Sessions


class DriversRepository:
    """
    Read-only repository for driver queries.
    
    Provides access to driver records, team assignments, and statistical data
    needed for market enrichment. No write operations (drivers managed via admin).
    """
    
    def __init__(self, session: Session, season: int):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy session for database operations
            season: Current season year for filtering results
        """
        self.session = session
        self.season = season
    
    def get_by_ids(self, driver_ids: list[int]) -> list[Drivers]:
        """
        Get drivers by list of IDs.
        
        Args:
            driver_ids: List of driver identifiers
            
        Returns:
            List of Driver models (may be fewer than input if some IDs don't exist)
        """
        if not driver_ids:
            return []
        
        drivers = []
        for driver_id in driver_ids:
            driver = self.session.exec(
                select(Drivers).where(Drivers.id == driver_id)
            ).first()
            if driver:
                drivers.append(driver)
        return drivers
    
    def get_team_assignments(self) -> Dict[int, str]:
        """
        Get driver→team map for current season (latest round per driver).
        
        Returns:
            Dictionary mapping driver_id to team_name
        """
        # Get latest round for the season
        latest_round = self.session.exec(
            select(func.max(DriverTeamLink.round_number))
            .where(DriverTeamLink.season_id == self.season)
        ).first()
        
        if not latest_round:
            return {}
        
        # Get driver-team assignments for latest round
        results = self.session.exec(
            select(DriverTeamLink.driver_id, Teams.team_name)
            .join(Teams, DriverTeamLink.team_id == Teams.id)  # type: ignore
            .where(
                DriverTeamLink.season_id == self.season,
                DriverTeamLink.round_number == latest_round
            )
        ).all()
        
        return {driver_id: team_name for driver_id, team_name in results}
    
    def get_driver_results_data(self) -> dict:
        """
        Get aggregate results data for stats calculations.
        
        Returns:
            Dictionary with keys:
            - max_round: Latest round number
            - sprint_rounds: List of sprint session records
            - results: List of driver total points
            - all_results: All session results for race/sprint sessions
        """
        max_round_result = self.session.exec(
            select(func.max(SessionResult.round_number))
        ).first()
        
        # Handle case where there are no results yet
        max_round = max_round_result if max_round_result else 0
        
        sprint_rounds = self.session.exec(
            select(Sessions)
            .where((Sessions.session_type == "Sprint") & (Sessions.round_number <= max_round))
        ).all()
        
        results = self.session.exec(
            select(
                SessionResult.driver_id,
                func.sum(SessionResult.points).label("total_points")
            )
            .where(SessionResult.round_number <= max_round)
            .group_by(SessionResult.driver_id)  # type: ignore
        ).all()
        
        all_results = self.session.exec(
            select(SessionResult)
            .where(
                (SessionResult.round_number <= max_round) &
                ((SessionResult.session_number == 5) | (SessionResult.session_number == 3))
            )
        ).all()
        
        return {
            "max_round": max_round,
            "sprint_rounds": sprint_rounds,
            "results": results,
            "all_results": all_results,
        }

    def get_active_driver_ids_for_season(self, season_year: int) -> list[int]:
        """Get IDs of all drivers active in the latest round of a season."""
        latest_round = self.session.exec(
            select(func.max(DriverTeamLink.round_number))
            .where(DriverTeamLink.season_id == season_year)
        ).first()
        if not latest_round:
            return []
        driver_ids = self.session.exec(
            select(DriverTeamLink.driver_id)
            .where(
                DriverTeamLink.season_id == season_year,
                DriverTeamLink.round_number == latest_round
            )
        ).all()
        return list(set(driver_ids))

    def get_all_drivers(self) -> list[Drivers]:
        """Get all drivers in the system."""
        return list(self.session.exec(select(Drivers)).all())

    def get_drivers_id_map(self) -> dict[int, int]:
        """Get mapping of driver_number -> driver.id for all drivers."""
        all_drivers = list(self.session.exec(select(Drivers)).all())
        return {driver.driver_number: driver.id for driver in all_drivers}

    def check_existing_drivers(self, driver: dict):
        """
        Check if a driver already exists and return updated model if changes detected,
        or a new Drivers instance if new. Returns None if driver exists and is unchanged.
        """
        existing = self.session.exec(
            select(Drivers).where(Drivers.driver_number == driver["driver_number"])
        ).first()
        if existing:
            existing_team = self._extract_team_from_url(existing.headshot_url)
            new_team = self._extract_team_from_url(driver["headshot_url"])
            needs_update = (
                existing.driver_color != driver["driver_color"] or
                existing_team != new_team
            )
            if needs_update:
                existing.driver_color = driver["driver_color"]
                if existing_team != new_team:
                    existing.headshot_url = driver["headshot_url"]
                return existing
            return None
        driver["current_market_value"] = 10_000_000
        return Drivers(**driver)

    def _extract_team_from_url(self, url: str) -> str:
        """Extract team name from headshot URL (index 4 in path split by '/')."""
        try:
            parts = url.split("/")
            if len(parts) >= 5:
                return parts[4]
            return ""
        except Exception:
            return ""
