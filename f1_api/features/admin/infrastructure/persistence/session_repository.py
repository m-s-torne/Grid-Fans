"""Session repository for admin data ingestion."""
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import Sessions


class SessionRepository:
    def __init__(self, session: Session, year: int):
        self.session = session
        self.season = year

    def get_existing_sessions(self) -> set[tuple]:
        """Get set of (round_number, session_number) tuples already stored for this season."""
        return set(self.session.exec(
            select(Sessions.round_number, Sessions.session_number)
            .where(Sessions.season_id == self.season)
        ).all())
