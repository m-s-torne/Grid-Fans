"""Drivers domain interfaces"""
from typing import Protocol, Dict
from f1_api.features.drivers.domain.models import Drivers


class DriversRepository(Protocol):
    """Repository interface for Drivers operations"""

    def get_by_ids(self, driver_ids: list[int]) -> list[Drivers]:
        """Get drivers by list of IDs."""
        ...

    def get_team_assignments(self) -> Dict[int, str]:
        """Get driver→team map for current season (latest round per driver)."""
        ...

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
        ...

    def get_active_driver_ids_for_season(self, season_year: int) -> list[int]:
        """Get IDs of all drivers active in the latest round of a season."""
        ...

    def get_all_drivers(self) -> list[Drivers]:
        """Get all drivers in the system."""
        ...

    def get_drivers_id_map(self) -> dict[int, int]:
        """Get mapping of driver_number -> driver.id for all drivers."""
        ...

    def check_existing_drivers(self, driver: dict) -> Drivers | None:
        """
        Check if a driver already exists and return updated model if changes detected,
        or a new Drivers instance if new. Returns None if driver exists and is unchanged.
        """
        ...
