"""Core F1 data domain interfaces."""
from typing import Protocol


class ISeasonContext(Protocol):
    """Protocol interface for season context operations."""

    @property
    def session_types_by_rn(self) -> dict: ...

    @property
    def session_map(self) -> dict: ...

    @property
    def schedule(self): ...

    def get_session_team_name_by_driver(self, driver, session) -> str: ...

    def get_session_teams(self, race) -> list: ...

    def get_drivers_by_team(self, team, race) -> set: ...

    def get_drivers_by_session(self, session) -> list: ...

    def driver_color(self, driver, session) -> str: ...


class DriverTeamLinkRepository(Protocol):
    """Repository interface for DriverTeamLink persistence operations."""

    def get_existing_links(self) -> set[tuple]:
        """
        Get set of (driver_id, team_id, round_number) tuples for all existing links.
        Used as a guard to avoid duplicate inserts during ingestion.
        """
        ...
