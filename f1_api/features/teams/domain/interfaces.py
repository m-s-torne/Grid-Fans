"""Teams domain interfaces"""
from typing import Protocol
from f1_api.features.teams.domain.models import Teams


class TeamsRepository(Protocol):
    """Repository interface for Teams operations"""

    def get_all_teams(self) -> list[Teams]:
        """Get all teams from database"""
        ...

    def get_team_points_data(self) -> list:
        """
        Get aggregated points data for all teams.

        Returns:
            List of tuples: (team_id, driver_id, round_number, round_points)
        """
        ...

    def get_team_id_map(self) -> dict[str, int]:
        """Get mapping of team_name -> team.id for all teams."""
        ...

    def get_existing_teams(self) -> set[str]:
        """Get set of existing team names."""
        ...
