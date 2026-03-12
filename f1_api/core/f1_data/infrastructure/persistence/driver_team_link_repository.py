"""DriverTeamLink repository - persistence queries for driver-team assignments"""
from sqlmodel import Session, select
from f1_api.features.drivers.domain.models import DriverTeamLink


class DriverTeamLinkRepository:
    """Repository for DriverTeamLink persistence operations."""

    def __init__(self, session: Session):
        self.session = session

    def get_existing_links(self) -> set[tuple]:
        """
        Get set of (driver_id, team_id, round_number) tuples for all existing links.
        Used as a guard to avoid duplicate inserts during ingestion.
        """
        return set(self.session.exec(
            select(DriverTeamLink.driver_id, DriverTeamLink.team_id, DriverTeamLink.round_number)
        ).all())
