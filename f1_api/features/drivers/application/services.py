"""Drivers application services"""
import logging
from sqlmodel import Session
from f1_api.features.drivers.domain.interfaces import DriversRepository
from f1_api.features.drivers.application.drivers_utility import DriversUtility

logger = logging.getLogger(__name__)


class GetDriversService:
    """
    Service for retrieving F1 drivers with their season statistics.
    
    Enriches driver data with calculated championship points, performance
    metrics, and rankings.
    """
    
    def __init__(self, drivers_repo: DriversRepository, session: Session):
        """
        Initialize service with repository and session.
        
        Args:
            drivers_repo: Repository for driver data access
            session: Database session for business logic operations
        """
        self.drivers_repo = drivers_repo
        self.session = session
        self.business_logic = DriversUtility()
    
    def execute(self) -> list:
        """
        Get all drivers sorted by championship points up to the last round.
        
        Returns:
            list: Drivers with calculated points and stats, empty list on error
        """
        try:
            database_data = self.drivers_repo.get_driver_results_data()
            max_round = database_data["max_round"]
            sprint_rounds = database_data["sprint_rounds"]
            results = database_data["results"]
            all_results = database_data["all_results"]
            db_drivers = self.drivers_repo.get_all_drivers()

            points_map = {r.driver_id: r.total_points for r in results}

            available_points = 25 * max_round + len(sprint_rounds) * 8

            stats = self.business_logic.get_driver_stats(all_results)
            
            drivers_sorted = sorted(
                db_drivers,
                key=lambda d: points_map.get(d.id, 0),
                reverse=True
            )

            drivers = self.business_logic.get_drivers_mapped(
                max_round, stats, points_map, available_points, drivers_sorted, self.session
            )

            return drivers
            
        except Exception as e:
            logger.warning("Drivers service execution interrupted: %s", e)
            return []
