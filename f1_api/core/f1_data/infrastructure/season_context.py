"""Season Context - Encapsulates season data loading logic"""
from datetime import datetime
from sqlmodel import Session, select
from f1_api.data_sources.ff1_client import FastF1Client
from f1_api.core.f1_data.domain.models import SessionResult


class SeasonContextController:
    """Controller to manage season context (schedule, session_map, registered rounds)"""
    def __init__(self, session: Session, ff1_client=FastF1Client):
        self.session = session
        self.ff1_client = ff1_client
        self.year = datetime.now().year
        self._schedule = None
        self._registered_rounds = None
        self._session_map = None
        self._session_types_by_rn = None

    @property
    def schedule(self):
        """Lazy load schedule"""
        if self._schedule is None:
            self._schedule = self.ff1_client.get_event_schedule(self.year)
            if self._schedule is None:
                raise RuntimeError(f"FastF1 returned no schedule for year {self.year}")
        return self._schedule

    @property
    def events_data(self):
        """Lazy load events data by round number"""
        events = []
        for _, e in self.schedule.iterrows():
            if e["EventFormat"] == "testing":
                continue
            event = {}
            event["round_number"] = e["RoundNumber"]
            event["event_name"] = e["EventName"]
            event["season_id"] = self.year
            event["event_type"] = e["EventFormat"]
            event["event_country"] = e["Country"]
            event["date_start"] = e["EventDate"].to_pydatetime()
            events.append(event)
        return events

    @property
    def registered_rounds(self):
        """Lazy load registered rounds for this season only"""
        if self._registered_rounds is None:
            self._registered_rounds = set(self.session.exec(
                select(SessionResult.round_number, SessionResult.session_number)
                .where(SessionResult.season_id == self.year)
            ).all())
        return self._registered_rounds

    @property
    def session_map(self):
        """Lazy load session map"""
        if self._session_map is None:
            self._session_map = self.ff1_client.get_session_map(self.year, self.registered_rounds)
        return self._session_map

    @property
    def session_types_by_rn(self):
        """Lazy load session types by round number"""
        if self._session_types_by_rn is None:
            self._session_types_by_rn = {}
            for _, event in self.schedule.iterrows():
                if event["EventFormat"] == "testing":
                    continue
                round_number = event["RoundNumber"]
                sessions = [
                    event["Session1"],
                    event["Session2"],
                    event["Session3"],
                    event["Session4"],
                    event["Session5"]
                ]
                self._session_types_by_rn[round_number] = sessions
        return self._session_types_by_rn

    def get_session_team_name_by_driver(self, driver, session):
        return self.ff1_client.get_session_team_name_by_driver(driver, session)

    def get_session_teams(self, race):
        return self.ff1_client.get_session_teams(race)

    def get_drivers_by_team(self, team, race):
        return self.ff1_client.get_drivers_by_team(team, race)

    def get_drivers_by_session(self, session):
        return self.ff1_client.get_drivers_by_session(session)

    def team_color(self, team_name, f1_session):
        """Gets team color"""
        return self.ff1_client.get_team_color(team_name, f1_session)

    def driver_color(self, driver, session):
        return self.ff1_client.get_driver_color(driver, session)

    def get_context(self):
        """Get all context data as a tuple"""
        return self.schedule, self.registered_rounds, self.session_map, self.session_types_by_rn


def get_season_context_service(session: Session) -> SeasonContextController:
    """Factory function for creating SeasonContextController"""
    return SeasonContextController(session)
