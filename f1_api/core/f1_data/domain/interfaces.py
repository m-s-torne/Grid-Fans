"""Core F1 data domain interfaces."""
from typing import Protocol


class DriverTeamLinkRepository(Protocol):
    """Repository interface for DriverTeamLink persistence operations."""

    def get_existing_links(self) -> set[tuple]:
        """
        Get set of (driver_id, team_id, round_number) tuples for all existing links.
        Used as a guard to avoid duplicate inserts during ingestion.
        """
        ...
