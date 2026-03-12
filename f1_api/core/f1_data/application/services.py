"""Drivers controller module for drivers-related operations"""
from datetime import datetime
import logging
from sqlmodel import Session
from f1_api.core.f1_data.infrastructure.season_context import SeasonContextController
from f1_api.data_sources.ff1_client import FastF1Client
from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.drivers.application.drivers_utility import DriversUtility
from f1_api.features.drivers.infrastructure.persistence import DriversRepository

class DriversController:
    """Provides drivers response"""
    def __init__(self, session: Session):
        self.session = session
        self.season = datetime.now().year
        self.repository = DriversRepository(session,self.season)
        self.business_logic = DriversUtility()
        self.season_context = SeasonContextController(session, FastF1Client)
    def get_drivers_service(self) -> list:
        """
        Get all drivers sorted by championship points up to the last round
        
        Args:
            session: Database session
            
        Returns:
            list: Drivers with calculated points and stats
        """
        try:
            database_data = self.repository.get_driver_results_data()
            max_round = database_data["max_round"]
            sprint_rounds = database_data["sprint_rounds"]
            results = database_data["results"]
            all_results = database_data["all_results"]
            db_drivers = self.repository.get_all_drivers()

            points_map = {r.driver_id: r.total_points for r in results}

            available_points = 25 * max_round + len(sprint_rounds) * 8

            stats = self.business_logic.get_driver_stats(all_results)
            
            drivers_sorted = sorted(
                db_drivers,
                key=lambda d: points_map.get(d.id, 0),
                reverse=True
            )

            drivers = self.business_logic.get_drivers_mapped(max_round, stats, points_map, available_points, drivers_sorted, self.session)

            return drivers
            
        except Exception as e:  # pylint: disable=broad-except
            logging.warning("Drivers controller execution interrupted by the following exception: %s", e)
            return []
    def get_driver_data(self) -> list[Drivers]:
        drivers_list = []
        added_drivers = set()
        session_types_by_rn = self.season_context.session_types_by_rn
        for round_number, session_types in session_types_by_rn.items():
            race = self.season_context.session_map.get((round_number,session_types[4]))
            accept_drivers = set()
            if race is not None:
                teams = self.season_context.get_session_teams(race)
                for t in teams:
                    accept_drivers.update(self.season_context.get_drivers_by_team(t,race))
            else:
                logging.warning(f"No race data available for round {round_number}, skipping driver processing for this round")
                continue
            for session_type in session_types:
                try:
                    f1_session = self.season_context.session_map.get((round_number,session_type))
                    if f1_session is None:
                        continue
                    results = f1_session.results
                    driver_names = self.season_context.get_drivers_by_session(f1_session)
                    for driver in driver_names:
                        if driver not in accept_drivers:
                            continue
                        driver_color = self.season_context.driver_color(driver,f1_session)
                        driver_number = results.loc[results["FullName"] == driver, "DriverNumber"].values[0] if not results.loc[results["FullName"] == driver, "DriverNumber"].empty else None
                        acronym = results.loc[results["FullName"] == driver, "Abbreviation"].values[0] if not results.loc[results["FullName"] == driver, "Abbreviation"].empty else None
                        country = results.loc[results["FullName"] == driver, "CountryCode"].values[0] if not results.loc[results["FullName"] == driver, "CountryCode"].empty else None
                        team = results.loc[results["FullName"] == driver, "TeamName"].values[0] if not results.loc[results["FullName"] == driver, "TeamName"].empty else None
                        team_name = team.lower().replace(" ", "")
                        driver_id = DriversUtility.create_driver_id(driver)
                        headshot_url = DriversUtility.get_driver_headshot_url(self.season,team_name,driver_id)
                        driver_key = (driver_number, team)
                        if driver_key in added_drivers:
                            continue
                        added_drivers.add(driver_key)
                        driver_obj = {
                            "driver_number": int(driver_number),
                            "full_name": driver,
                            "acronym": acronym,
                            "driver_color": driver_color,
                            "country_code": country,
                            "headshot_url": headshot_url
                        }
                        updated_driver = self.repository.check_existing_drivers(driver_obj)
                        if updated_driver:
                            drivers_list.append(updated_driver)
                except Exception as e:
                    logging.warning(f"Round {round_number} not availavle yet: {e}")
                    return drivers_list
        return drivers_list
    def get_drivers_id_map(self):
        all_drivers = self.repository.get_all_drivers()
        driver_id_map = {driver.driver_number: driver.id for driver in all_drivers}
        return driver_id_map
def get_drivers_service(session: Session) -> list:
    """
    Legacy function for getting drivers
    """
    controller = DriversController(session)
    return controller.get_drivers_service()
def get_driver_data(session):
    drivers_controller = DriversController(session)
    return drivers_controller.get_driver_data()
def get_drivers_id_map(session):
    drivers_controller = DriversController(session)
    return drivers_controller.get_drivers_id_map()
