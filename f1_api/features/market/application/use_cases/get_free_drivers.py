"""Use case: Get free agent drivers with enrichment"""
from typing import Dict, Any
import logging

from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.market.domain.services import DriverEnrichmentService
from f1_api.features.drivers.application.drivers_utility import DriversUtility

logger = logging.getLogger(__name__)


class GetFreeDriversUseCase:
    """
    Query use case for retrieving all free agent drivers in a league.
    
    Returns enriched driver data including season stats, fantasy stats,
    ownership information, and market metadata. Free agents are drivers
    without an owner (owner_id = None).
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
    
    def execute(self, league_id: int) -> list[Dict[str, Any]]:
        """
        Execute query for free agent drivers.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of enriched driver dictionaries with ownership and stats
        """
        logger.info("Fetching free drivers for league %d", league_id)
        
        # Get free agent ownerships
        ownerships = self.ownership_repo.get_free_drivers_in_league(league_id)
        
        if not ownerships:
            logger.info("No free drivers found in league %d", league_id)
            return []
        
        # Get driver records
        driver_ids = [o.driver_id for o in ownerships]
        drivers = self.drivers_repo.get_by_ids(driver_ids)
        
        if not drivers:
            logger.warning("No driver records found for free agents in league %d", league_id)
            return []
        
        # Get stats data
        driver_results_data = self.drivers_repo.get_driver_results_data()
        team_map = self.drivers_repo.get_team_assignments()
        
        # Enrich driver list
        enriched_drivers = DriverEnrichmentService.enrich_driver_list(
            drivers=drivers,
            ownerships=ownerships,
            driver_results_data=driver_results_data,
            drivers_utility=self.drivers_utility,
            team_map=team_map,
            is_owned=False,
            is_owned_by_me=False,
            is_free_agent=True,
            is_for_sale=False,
            include_owner_names=False,
        )
        
        logger.info("Returning %d free drivers for league %d", len(enriched_drivers), league_id)
        return enriched_drivers
