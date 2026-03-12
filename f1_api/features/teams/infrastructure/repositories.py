"""Teams infrastructure - repository implementation"""
from sqlmodel import Session, select, func
from f1_api.features.teams.domain.models import Teams
from f1_api.features.drivers.domain.models import DriverTeamLink
from f1_api.core.f1_data.domain.models import SessionResult


class TeamsRepository:
    """Repository for team queries."""

    def __init__(self, session: Session):
        self.session = session

    def get_all_teams(self) -> list[Teams]:
        """Get all teams from database"""
        teams = list(self.session.exec(select(Teams)))
        return teams

    def get_team_points_data(self) -> list:
        """
        Get aggregated points data for all teams.

        Returns:
            List of tuples: (team_id, driver_id, round_number, round_points)
        """
        return self.session.exec(
            select(
                DriverTeamLink.team_id,
                DriverTeamLink.driver_id,
                DriverTeamLink.round_number,
                func.sum(SessionResult.points).label("round_points")
            )
            .join(SessionResult,
                (SessionResult.driver_id == DriverTeamLink.driver_id) &
                (SessionResult.round_number == DriverTeamLink.round_number))
            .group_by(
                DriverTeamLink.team_id,
                DriverTeamLink.driver_id,
                DriverTeamLink.round_number
            )
        ).all()

    def get_team_id_map(self) -> dict[str, int]:
        """Get mapping of team_name -> team.id for all teams."""
        all_teams = list(self.session.exec(select(Teams)).all())
        return {team.team_name: team.id for team in all_teams}

    def get_existing_teams(self) -> set[str]:
        """Get set of existing team names."""
        return set(self.session.exec(select(Teams.team_name)).all())
