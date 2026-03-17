"""This layer connects the API to the external FastF1 service"""
from datetime import datetime
from typing import Optional
import logging
import fastf1 as ff1
from fastf1 import plotting
from fastf1.events import EventSchedule

class FastF1Client:
    """Base client for FastF1 API communication"""
    @staticmethod
    def get_event_schedule(year: int) -> Optional[EventSchedule]:
        """Get event schedule for a year"""
        try:
            return ff1.get_event_schedule(year)
        except Exception as e:
            logging.error(f"Error getting schedule for {year}: {e}")
            return None
    @staticmethod
    def get_session_map(year: int, existing_rounds: set[tuple[int, int]]) -> dict:
        """Loads all sessions and returns them in a Dic"""
        session_map = {}
        schedule = FastF1Client.get_event_schedule(year)
        if schedule is None:
            logging.error(f"Could not retrieve schedule for {year}, aborting session load.")
            return session_map
        today = datetime.now().date()
        for _, event in schedule.iterrows():
            if event["EventFormat"] == "testing":
                continue
            event_date = event["EventDate"]
            if hasattr(event_date, "date") and event_date.date() > today:
                logging.info(f"Skipping future event: {event['EventName']} (scheduled {event_date.date()})")
                continue
            rn = event["RoundNumber"]
            name = event["EventName"]
            sessions = [
                event["Session1"],
                event["Session2"],
                event["Session3"],
                event["Session4"],
                event["Session5"]
            ]
            for sn, session_type in enumerate(sessions, start=1):
                if (rn, sn) in existing_rounds:
                    logging.info(f"{event['EventName']} session {sn} already in DB")
                    continue
                try:
                    f1_session = ff1.get_session(year=year, gp=name, identifier=session_type)
                    f1_session.load(laps=True, telemetry=False, weather=False, messages=False)
                except Exception as e:
                    logging.warning(f"Failed to load session {session_type} at {name}: {e}")
                    continue
                if f1_session.results.empty:
                    logging.warning(f"No data for session {session_type} at {name}, skipping.")
                    continue
                session_map[(rn, session_type)] = f1_session
        return session_map
    @staticmethod
    def get_session_team_name_by_driver(driver, session):
        try:
            return plotting.get_team_name_by_driver(driver, session)
        except (KeyError, Exception):
            match = session.results.loc[session.results["Abbreviation"] == driver, "TeamName"]
            if not match.empty:
                return match.values[0]
            raise
    @staticmethod
    def _fallback_team_color(team_name: str) -> str:
        """Look up team color from the most recent available Constants year."""
        try:
            from fastf1.plotting._backend import Constants
            latest_year = sorted(Constants.keys())[-1]
            teams = Constants[latest_year].Teams
            key = team_name.lower()
            if key in teams:
                return teams[key].TeamColor.Official
            for k in teams:
                if k in key or key in k:
                    return teams[k].TeamColor.Official
        except Exception:
            pass
        return "#FFFFFF"

    @staticmethod
    def get_team_color(team_name: str, f1_session):
        """Gets team color"""
        try:
            return plotting.get_team_color(team_name, f1_session)
        except (KeyError, Exception):
            return FastF1Client._fallback_team_color(team_name)
    @staticmethod
    def get_session_teams(race):
        try:
            return plotting.list_team_names(race)
        except (KeyError, Exception):
            return race.results["TeamName"].dropna().unique().tolist()
    @staticmethod
    def get_drivers_by_team(team, race):
        try:
            return plotting.get_driver_names_by_team(identifier=team, session=race)
        except (KeyError, Exception):
            return race.results.loc[race.results["TeamName"] == team, "FullName"].tolist()
    @staticmethod
    def get_drivers_by_session(session):
        try:
            return plotting.list_driver_names(session)
        except (KeyError, Exception):
            return session.results["FullName"].dropna().tolist()
    @staticmethod
    def get_driver_color(driver, session):
        try:
            return plotting.get_driver_color(driver, session)
        except (KeyError, Exception):
            match = session.results.loc[session.results["Abbreviation"] == driver, "TeamName"]
            team_name = match.values[0] if not match.empty else ""
            return FastF1Client._fallback_team_color(team_name)
def load_sessions(year,existing):
    return FastF1Client.get_session_map(year=year,existing_rounds=existing)