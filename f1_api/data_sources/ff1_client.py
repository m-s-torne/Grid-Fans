"""This layer connects the API to the external FastF1 service"""
from typing import Optional
import logging
import fastf1 as ff1
from fastf1 import plotting
from fastf1.events import EventSchedule

class SessionLoadError(Exception):
    """
    Custom exception for fastf1 session loading errors
    """

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
        try:
            schedule = FastF1Client.get_event_schedule(year)
            if schedule is None:
                logging.error(f"Could not retrieve schedule for {year}, aborting session load.")
                return session_map
            for _,event in schedule.iloc[1:].iterrows():
                rn = event["RoundNumber"]
                if event["EventFormat"] == "testing":
                    continue
                name = event["EventName"]
                sessions = [
                    event["Session1"],
                    event["Session2"],
                    event["Session3"],
                    event["Session4"],
                    event["Session5"]
                ]
                for sn,session_type in enumerate(sessions,start=1):
                    if (rn,sn) in existing_rounds:
                        logging.info(f"{event["EventName"]} session {sn} already in DB")
                        continue
                    try:
                        f1_session = ff1.get_session(year=year,gp=name,identifier=session_type)
                        f1_session.load(laps=True, telemetry=False, weather=False, messages=False)
                    except Exception as e:
                        logging.warning(f"Failed to load session {session_type} at {name}: {e}")
                        continue
                    if f1_session.results.empty:
                        logging.warning(f"No data for session {session_type} at {name}, skipping.")
                        raise SessionLoadError("No more sessions to load")
                    session_map[(rn, session_type)] = f1_session
            return session_map
        except SessionLoadError:
            logging.warning("Stopped loading further sessions")
            return session_map
    @staticmethod
    def get_session_team_name_by_driver(driver,session):
        return plotting.get_team_name_by_driver(driver,session)
    @staticmethod
    def get_team_color(team_name: str, f1_session):
        """Gets team color"""
        return plotting.get_team_color(team_name, f1_session)
    @staticmethod
    def get_session_teams(race):
        return plotting.list_team_names(race)
    @staticmethod
    def get_drivers_by_team(team, race):
        return plotting.get_driver_names_by_team(identifier=team,session=race)
    @staticmethod
    def get_drivers_by_session(session):
        return plotting.list_driver_names(session)
    @staticmethod
    def get_driver_color(driver,session):
        return plotting.get_driver_color(driver,session)
def load_sessions(year,existing):
    return FastF1Client.get_session_map(year=year,existing_rounds=existing)