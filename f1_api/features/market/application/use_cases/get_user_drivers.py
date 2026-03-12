"""Use case: Get user's drivers with enrichment"""
from typing import Dict, Any
import logging

from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.market.domain.services import DriverEnrichmentService
from f1_api.features.drivers.application.drivers_utility import DriversUtility

logger = logging.getLogger(__name__)


class GetUserDriversUseCase:
    """
    Query use case for retrieving all drivers owned by a specific user.
    
    Returns enriched driver data including season stats, fantasy stats,
    and ownership information. Marks isOwnedByMe=True and respects
    individual driver's is_listed_for_sale status.
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        drivers_repo: DriversRepository,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            drivers_repo: Repository for driver data and stats
        """
        self.ownership_repo = ownership_repo
        self.drivers_repo = drivers_repo
        self.drivers_utility = DriversUtility()
    
    def execute(self, user_id: int, league_id: int) -> list[Dict[str, Any]]:
        """
        Execute query for user's drivers.
        
        Args:
            user_id: User identifier (internal user ID)
            league_id: League identifier
            
        Returns:
            List of enriched driver dictionaries with ownership info
        """
        try:
            logger.info("Fetching drivers for user %d in league %d", user_id, league_id)
            
            # Get user's ownerships
            ownerships = self.ownership_repo.get_owned_by_user_in_league(user_id, league_id)
            logger.debug("Found %d ownerships", len(ownerships))
            
            if not ownerships:
                logger.info("No drivers owned by user %d in league %d", user_id, league_id)
                return []
            
            # Get driver records
            driver_ids = [o.driver_id for o in ownerships]
            logger.debug("Looking up driver IDs: %s", driver_ids)
            drivers = self.drivers_repo.get_by_ids(driver_ids)
            logger.debug("Found %d drivers", len(drivers))
            
            if not drivers:
                logger.warning("No driver records found for user %d's drivers in league %d", user_id, league_id)
                return []
            
            # Get stats data
            logger.debug("Fetching driver results data")
            driver_results_data = self.drivers_repo.get_driver_results_data()
            logger.debug("Fetching team assignments")
            team_map = self.drivers_repo.get_team_assignments()
            
            # Enrich driver list
            logger.debug("Enriching driver list")
            enriched_drivers = DriverEnrichmentService.enrich_driver_list(
                drivers=drivers,
                ownerships=ownerships,
                driver_results_data=driver_results_data,
                drivers_utility=self.drivers_utility,
                team_map=team_map,
                is_owned=True,
                is_owned_by_me=True,
                is_free_agent=False,
                is_for_sale=False,  # Will be overridden per-driver by ownership.is_listed_for_sale
                include_owner_names=False,
            )
            
            logger.info("Returning %d drivers for user %d in league %d", len(enriched_drivers), user_id, league_id)
            return enriched_drivers
        except Exception as e:
            logger.error("Error in GetUserDriversUseCase: %s", str(e), exc_info=True)
            raise
