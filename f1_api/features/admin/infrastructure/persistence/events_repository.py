"""Events repository for admin data ingestion."""
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import Events


class EventsRepository:
    def __init__(self, session: Session, year: int):
        self.session = session
        self.season = year

    def get_round_numbers(self) -> set[int]:
        """Get set of round numbers already stored for this season."""
        return set(self.session.exec(
            select(Events.round_number).where(Events.season_id == self.season)
        ).all())
