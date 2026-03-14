"""
Admin data ingestion utilities.
Provides functions to fetch F1 data for season database updates.
"""
import logging
import math
import pandas as pd
from sqlmodel import Session
from fastf1 import plotting
from f1_api.core.f1_data.infrastructure.season_context import SeasonContextController
from f1_api.data_sources.ff1_client import FastF1Client
from f1_api.core.f1_data.domain.models import Events, Sessions, SessionResult
from f1_api.features.teams.domain.models import Teams
from f1_api.features.admin.infrastructure.persistence.events_repository import EventsRepository
from f1_api.features.admin.infrastructure.persistence.session_repository import SessionRepository
from f1_api.features.admin.infrastructure.persistence.session_results_repository import SessionResultsRepository
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.teams.infrastructure.repositories import TeamsRepository


def get_event_data(session: Session, year: int) -> list[Events]:
    """Returns new Events to insert for the given season year."""
    repository = EventsRepository(session, year)
    season_context = SeasonContextController(session)
    round_numbers = repository.get_round_numbers()
    events = []
    for e in season_context.events_data:
        if e["round_number"] in round_numbers:
            continue
        events.append(Events(
            round_number=e["round_number"],
            season_id=e["season_id"],
            event_name=e["event_name"],
            event_type=e["event_type"],
            event_country=e["event_country"],
            date_start=e["date_start"]
        ))
    return events


def get_session_data(session: Session, year: int) -> list[Sessions]:
    """Returns new Sessions to insert for the given season year."""
    repository = SessionRepository(session, year)
    season_context = SeasonContextController(session)
    existing_sessions = repository.get_existing_sessions()
    sessions = []
    for round_number, session_types in season_context.session_types_by_rn.items():
        for i, session_type in enumerate(session_types, start=1):
            if (round_number, i) in existing_sessions:
                continue
            sessions.append(Sessions(
                round_number=round_number,
                season_id=year,
                session_number=i,
                session_type=session_type
            ))
    return sessions


def get_session_results(year: int, session: Session) -> list[SessionResult]:
    """Returns new SessionResults to insert for the given season year."""
    repository = SessionResultsRepository(session, year)
    season_context = SeasonContextController(session, FastF1Client)
    drivers_repository = DriversRepository(session, year)
    teams_repository = TeamsRepository(session)

    session_results = []
    existing_results = repository.get_registered_results()
    session_map = season_context.session_map
    session_types_by_rn = season_context.session_types_by_rn

    for round_number, session_types in session_types_by_rn.items():
        for session_number, session_type in enumerate(session_types, start=1):
            try:
                f1_session = session_map.get((round_number, session_type))
                if f1_session is None:
                    continue

                driver_list = f1_session.drivers
                results = f1_session.results
                laps = f1_session.laps

                if session_type in ("Sprint", "Race"):
                    fastest_driver = laps.pick_fastest()["Driver"]
                    disq_drivers = results.loc[results["Status"] == "Disqualified", "Abbreviation"]
                    if fastest_driver in disq_drivers.values:
                        laps = laps[laps["Driver"] != fastest_driver]

                for driver_num in driver_list:
                    driver_name = results.loc[results["DriverNumber"] == driver_num, "Abbreviation"].values[0]

                    try:
                        team_name = season_context.get_session_team_name_by_driver(driver_name, f1_session)
                    except Exception as e:
                        logging.warning(f"Skipping driver {driver_name}: {e}")
                        continue

                    team_id = teams_repository.get_team_id_map().get(team_name)
                    driver_id = drivers_repository.get_drivers_id_map().get(int(driver_num))

                    if driver_id is None or team_id is None:
                        continue

                    driver_results = f1_session.get_driver(driver_name)
                    position = None
                    grid_position = None
                    fastest = None
                    driver_lap = laps.pick_drivers(driver_name).pick_fastest()
                    if driver_lap is not None:
                        fastest = driver_lap["LapTime"].total_seconds()
                    total_time = None
                    status = None
                    points = None
                    fastest_lap = None

                    if session_type in ("Sprint", "Race"):
                        position = str(driver_results["ClassifiedPosition"])
                        grid_position = int(driver_results["GridPosition"])
                        raw_time = driver_results["Time"]
                        if pd.isna(raw_time):
                            total_time = None
                        else:
                            total_time = raw_time.total_seconds()
                            if math.isnan(total_time):
                                total_time = None
                        points = int(driver_results["Points"])
                        status = driver_results["Status"]
                        session_fastest = laps["LapTime"].min().total_seconds()
                        classified = str(driver_results["ClassifiedPosition"])
                        if classified.isdigit():
                            fastest_lap = fastest == session_fastest
                        else:
                            fastest_lap = False

                    if session_type == "Qualifying":
                        position = str(driver_results["Position"])

                    if (round_number, session_number, driver_id) in existing_results:
                        continue

                    session_results.append(SessionResult(
                        season_id=year,
                        round_number=round_number,
                        session_number=session_number,
                        driver_id=driver_id,
                        position=position,
                        grid_position=grid_position,
                        best_lap_time=fastest,
                        total_time=total_time,
                        points=points,
                        status=status,
                        fastest_lap=fastest_lap
                    ))
            except Exception as e:
                logging.warning(f"Skipping session {session_type} for round {round_number} in year {year}: {e}")
    return session_results


def get_team_data(session: Session) -> list[Teams]:
    """Returns new Teams to insert from season data."""
    season_context = SeasonContextController(session, FastF1Client)
    repository = TeamsRepository(session)

    teams = []
    existing_teams = repository.get_existing_teams() or set()
    session_types_by_rn = season_context.session_types_by_rn
    added_teams: set[str] = set()

    for round_number, session_types in session_types_by_rn.items():
        for session_type in session_types:
            try:
                f1_session = season_context.session_map.get((round_number, session_type))
                if f1_session is None:
                    continue

                try:
                    team_names = plotting.list_team_names(f1_session)
                except Exception as e:
                    logging.warning(f"Could not get team names for round {round_number}, {session_type}: {e}")
                    continue

                for name in team_names:
                    if name in existing_teams or name in added_teams:
                        continue
                    added_teams.add(name)
                    try:
                        color = season_context.team_color(name, f1_session)
                    except Exception:
                        color = "#FFFFFF"
                    teams.append(Teams(team_name=name, team_color=color))

            except Exception as e:
                logging.warning(f"Error processing round {round_number}, {session_type}: {e}")

    return teams
