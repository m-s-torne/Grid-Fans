"""Infrastructure implementations for DriverTeamLink data fetching and reconciliation."""
import logging
import fastf1 as ff1
from fastf1.events import EventSchedule
from sqlmodel import Session, select
from f1_api.core.f1_data.domain.models import SessionResult
from f1_api.features.drivers.domain.models import DriverTeamLink
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.teams.domain.interfaces import TeamsRepository as ITeamsRepository
from f1_api.core.f1_data.domain.interfaces import DriverTeamLinkRepository as IDriverTeamLinkRepository, ISeasonContext
from f1_api.core.f1_data.application.driver_team_link_service import DriverTeamLinkController


def get_all_driver_team_links(
    year: int,
    driver_repo: IDriversRepository,
    team_repo: ITeamsRepository,
    link_repo: IDriverTeamLinkRepository,
    season_context: ISeasonContext,
) -> list[DriverTeamLink]:
    controller = DriverTeamLinkController(
        driver_repository=driver_repo,
        team_repository=team_repo,
        repository=link_repo,
        season_context=season_context,
        season=year,
    )
    return controller.get_all_driver_team_links()


async def reconcile_driver_team_links(
    session: Session,
    year: int,
    driver_repo: IDriversRepository,
    team_repo: ITeamsRepository,
    link_repo: IDriverTeamLinkRepository,
    season_context: ISeasonContext,
) -> list[DriverTeamLink]:
    """
    Reconciles missing DriverTeamLinks for SessionResults that exist.

    1. Identifies rounds that have SessionResults but no DriverTeamLinks
    2. Loads the necessary F1 session data for those rounds
    3. Creates the missing DriverTeamLink entries

    Returns:
        list[DriverTeamLink]: List of newly created DriverTeamLink objects
    """
    rounds_with_results = set(session.exec(
        select(SessionResult.round_number).distinct()
    ).all())

    rounds_with_links = set(session.exec(
        select(DriverTeamLink.round_number).distinct()
    ).all())

    missing_rounds = rounds_with_results - rounds_with_links

    if not missing_rounds:
        logging.info("All rounds have DriverTeamLinks, no reconciliation needed")
        return []

    logging.warning(f"Missing DriverTeamLinks for rounds: {sorted(missing_rounds)}")

    driver_team_links = []
    existing_links = link_repo.get_existing_links()
    links_set = set()

    for round_number in sorted(missing_rounds):
        logging.info(f"Reconciling round {round_number}")

        session_types = season_context.session_types_by_rn.get(round_number)
        if not session_types:
            logging.warning(f"No session types found for round {round_number}")
            continue

        try:
            schedule: EventSchedule | None = season_context.schedule  # type: ignore[assignment]
            if schedule is None:
                logging.warning(f"No schedule available for round {round_number}")
                continue
            event_row = schedule[schedule["RoundNumber"] == round_number]
            if event_row.empty:
                logging.warning(f"No event found for round {round_number}")
                continue
            event_name = event_row["EventName"].values[0]
        except Exception as e:
            logging.warning(f"Could not get event name for round {round_number}: {e}")
            continue

        for session_type in session_types:
            try:
                f1_session = ff1.get_session(year=year, gp=event_name, identifier=session_type)
                f1_session.load(laps=False, telemetry=False, weather=False, messages=False)

                if f1_session.results.empty:
                    logging.info(f"No results for {session_type} at {event_name}")
                    continue

                driver_list = f1_session.drivers
                results = f1_session.results

                for driver_num in driver_list:
                    try:
                        driver_id = driver_repo.get_drivers_id_map().get(int(driver_num))
                        if driver_id is None:
                            logging.debug(f"Driver {driver_num} not found in database")
                            continue

                        abb_match = results.loc[results["DriverNumber"] == driver_num, "Abbreviation"]
                        if abb_match.empty:
                            logging.debug(f"No abbreviation found for driver {driver_num}")
                            continue
                        driver_abb = str(abb_match.iloc[0])
                        team_name = season_context.get_session_team_name_by_driver(driver_abb, f1_session)
                        team_id = team_repo.get_team_id_map().get(team_name)

                        if team_id is None:
                            logging.debug(f"Team {team_name} not found in database")
                            continue

                        if (driver_id, team_id, round_number) in existing_links:
                            continue

                        link_key = (driver_id, team_id, round_number)
                        if link_key in links_set:
                            continue

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
