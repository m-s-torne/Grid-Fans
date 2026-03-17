"""Session results repository for admin data ingestion."""
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import SessionResult


class SessionResultsRepository:
    def __init__(self, session: Session, year: int):
        self.session = session
        self.season = year

    def get_registered_rounds(self) -> set[int]:
        """Get set of round numbers that have session results for this season."""
        return set(self.session.exec(
            select(SessionResult.round_number).where(SessionResult.season_id == self.season)
        ).all())

    def get_registered_results(self) -> set[tuple]:
        """Get set of (round_number, session_number, driver_id) tuples already stored for this season."""
        existing = self.session.exec(
            select(SessionResult.round_number, SessionResult.session_number, SessionResult.driver_id)
            .where(SessionResult.season_id == self.season)
        ).all()
        return set(existing)
