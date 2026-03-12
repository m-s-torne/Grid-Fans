"""
Reconciliation logic for DriverTeamLinks.

This module handles the detection and creation of missing DriverTeamLinks
when SessionResults exist but the corresponding links were not created.
"""
import logging
import fastf1 as ff1
from sqlmodel import Session, select
from f1_api.core.f1_data.infrastructure.season_context import SeasonContextController
from f1_api.data_sources.ff1_client import FastF1Client
from f1_api.core.f1_data.domain.models import SessionResult
from f1_api.features.drivers.domain.models import DriverTeamLink
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.teams.infrastructure.repositories import TeamsRepository
from f1_api.core.f1_data.infrastructure.persistence.driver_team_link_repository import DriverTeamLinkRepository


async def reconcile_driver_team_links(session: Session, year: int):
    """
    Reconciles missing DriverTeamLinks for SessionResults that exist.
    
    This function:
    1. Identifies rounds that have SessionResults but no DriverTeamLinks
    2. Loads the necessary F1 session data for those rounds
    3. Creates the missing DriverTeamLink entries
    
    Args:
        session: Database session
        year: Season year to reconcile
        
    Returns:
        list[DriverTeamLink]: List of newly created DriverTeamLink objects
    """
    # 1. Get rounds with SessionResults
    rounds_with_results = set(session.exec(
        select(SessionResult.round_number).distinct()
    ).all())
    
    # 2. Get rounds with DriverTeamLinks
    rounds_with_links = set(session.exec(
        select(DriverTeamLink.round_number).distinct()
    ).all())
    
    # 3. Find rounds with SessionResults but WITHOUT DriverTeamLinks
    missing_rounds = rounds_with_results - rounds_with_links
    
    if not missing_rounds:
        logging.info("All rounds have DriverTeamLinks, no reconciliation needed")
        return []
    
    logging.warning(f"Missing DriverTeamLinks for rounds: {sorted(missing_rounds)}")
    
    # 4. Create DriverTeamLinks only for the missing rounds
    driver_team_links = []
    season_context = SeasonContextController(session, FastF1Client)
    driver_repo = DriversRepository(session, year)
    team_repo = TeamsRepository(session)
    link_repo = DriverTeamLinkRepository(session)
    existing_links = link_repo.get_existing_links()
    
    links_set = set()  # Track links in this batch to avoid duplicates
    
    for round_number in sorted(missing_rounds):
        logging.info(f"Reconciling round {round_number}")
        
        # Get session types for this round
        session_types = season_context.session_types_by_rn.get(round_number)
        if not session_types:
            logging.warning(f"No session types found for round {round_number}")
            continue
        
        # Get event name for this round
        try:
            schedule = season_context.schedule
            event_row = schedule[schedule["RoundNumber"] == round_number]
            if event_row.empty:
                logging.warning(f"No event found for round {round_number}")
                continue
            event_name = event_row["EventName"].values[0]
        except Exception as e:
            logging.warning(f"Could not get event name for round {round_number}: {e}")
            continue
        
        # Process each session type
        for session_type in session_types:
            try:
                # Load session directly (bypass session_map cache)
                f1_session = ff1.get_session(year=year, gp=event_name, identifier=session_type)
                f1_session.load(laps=False, telemetry=False, weather=False, messages=False)
                
                if f1_session.results.empty:
                    logging.info(f"No results for {session_type} at {event_name}")
                    continue
                
                driver_list = f1_session.drivers
                results = f1_session.results
                
                # Process each driver
                for driver_num in driver_list:
                    try:
                        driver_id = driver_repo.get_drivers_id_map().get(int(driver_num))
                        if driver_id is None:
                            logging.debug(f"Driver {driver_num} not found in database")
                            continue
                        
                        driver_abb = results.loc[results["DriverNumber"] == driver_num, "Abbreviation"].values[0]
                        team_name = season_context.get_session_team_name_by_driver(driver_abb, f1_session)
                        team_id = team_repo.get_team_id_map().get(team_name)
                        
                        if team_id is None:
                            logging.debug(f"Team {team_name} not found in database")
                            continue
                        
                        # Check if link already exists in DB
                        if (driver_id, team_id, round_number) in existing_links:
                            continue
                        
                        # Check if link already in this batch
                        link_key = (driver_id, team_id, round_number)
                        if link_key in links_set:
                            continue
                        
                        # Create new link
                        driver_team_links.append(DriverTeamLink(
                            driver_id=driver_id,
                            team_id=team_id,
                            season_id=year,
                            round_number=round_number
                        ))
                        links_set.add(link_key)
                        logging.debug(f"Created link: driver={driver_id}, team={team_id}, round={round_number}")
                        
                    except Exception as e:
                        logging.warning(f"Skipping driver {driver_num} in {session_type}: {e}")
                        continue
                
                # We only need to process ONE session per round to get all driver-team assignments
                # Once we successfully process one session, break to avoid redundant work
                if driver_team_links:
                    logging.info(f"Created {len([l for l in driver_team_links if l.round_number == round_number])} links for round {round_number}")
                    break
                        
            except Exception as e:
                logging.warning(f"Could not load session {session_type} for round {round_number}: {e}")
                continue
    
    if driver_team_links:
        logging.info(f"Reconciliation complete: created {len(driver_team_links)} missing DriverTeamLinks")
    else:
        logging.warning("Reconciliation complete: no new links created")
    
    return driver_team_links
