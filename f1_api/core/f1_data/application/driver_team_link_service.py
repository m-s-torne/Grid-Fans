import logging
from sqlmodel import Session
from f1_api.features.drivers.domain.interfaces import DriversRepository as IDriversRepository
from f1_api.features.teams.domain.interfaces import TeamsRepository as ITeamsRepository
from f1_api.core.f1_data.domain.interfaces import DriverTeamLinkRepository as IDriverTeamLinkRepository
from f1_api.features.drivers.domain.models import DriverTeamLink

class DriverTeamLinkController:
    def __init__(
        self,
        driver_repository: IDriversRepository,
        team_repository: ITeamsRepository,
        repository: IDriverTeamLinkRepository,
        season_context,
        season: int,
    ):
        self.season = season
        self.driver_repository = driver_repository
        self.team_repository = team_repository
        self.repository = repository
        self.season_context = season_context
    def get_all_driver_team_links(self) -> list[DriverTeamLink]:
        """
        Returns a list of DriverTeamLink objects for all (driver, team, round) assignments
        """
        links = set()
        driver_team_links = []
        existing_links = self.repository.get_existing_links()
        session_types_by_rn = self.season_context.session_types_by_rn
        for round_number, session_types in session_types_by_rn.items():
            for session_number,session_type in enumerate(session_types, start=1):
                try:
                    f1_session = self.season_context.session_map.get((round_number, session_type))           
                    # Skip if session data not available
                    if f1_session is None:
                        continue   
                    driver_list = f1_session.drivers
                    results = f1_session.results
                    for driver_num in driver_list:
                        try:
                            driver_id = self.driver_repository.get_drivers_id_map().get(int(driver_num))
                            driver_abb = results.loc[results["DriverNumber"] == driver_num, "Abbreviation"].values[0]
                            team_name = self.season_context.get_session_team_name_by_driver(driver_abb,f1_session)
                            team_id = self.team_repository.get_team_id_map().get(team_name)
                            if (driver_id, team_id, round_number) in existing_links:
                                continue
                            if driver_id is None or team_id is None:
                                continue
                            link_key = (driver_id, team_id, self.season, round_number)
                            if link_key in links:
                                continue
                            driver_team_links.append(DriverTeamLink(
                                driver_id=driver_id,
                                team_id=team_id,
                                season_id=self.season,
                                round_number=round_number
                            ))
                            links.add(link_key)
                        except Exception as e:
                            logging.warning(f"Skipping driver {driver_num} in session {session_type}: {e}")
                            continue
                except Exception as e:
                    logging.warning(f"Round {round_number} not availavle yet: {e}")
                    continue
        return driver_team_links
def get_all_driver_team_links(
    session: Session,
    year: int,
    driver_repo: IDriversRepository,
    team_repo: ITeamsRepository,
    link_repo: IDriverTeamLinkRepository,
    season_context,
) -> list[DriverTeamLink]:
    controller = DriverTeamLinkController(
        driver_repository=driver_repo,
        team_repository=team_repo,
        repository=link_repo,
        season_context=season_context,
        season=year,
    )
    return controller.get_all_driver_team_links()