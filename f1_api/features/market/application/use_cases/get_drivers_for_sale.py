"""Use case: Get drivers listed for sale with owner info"""
from typing import Dict, Any
import logging

from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.drivers.infrastructure.persistence import DriversRepository
from f1_api.features.market.domain.services import DriverEnrichmentService
from f1_api.features.drivers.application.drivers_utility import DriversUtility
from f1_api.features.user.infrastructure.repositories import UserRepositoryImpl

logger = logging.getLogger(__name__)


class GetDriversForSaleUseCase:
    """
    Query use case for retrieving all drivers listed for sale in a league.
    
    Returns enriched driver data including season stats, fantasy stats,
    ownership information, and seller names. Only includes drivers where
    is_listed_for_sale = True.
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        drivers_repo: DriversRepository,
        users_repo: UserRepositoryImpl,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            drivers_repo: Repository for driver data and stats
            users_repo: Repository for user data (for owner names)
        """
        self.ownership_repo = ownership_repo
        self.drivers_repo = drivers_repo
        self.users_repo = users_repo
        self.drivers_utility = DriversUtility()
    
    def execute(self, league_id: int) -> list[Dict[str, Any]]:
        """
        Execute query for drivers listed for sale.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of enriched driver dictionaries with ownership and seller info
        """
        logger.info("Fetching drivers for sale in league %d", league_id)
        
        # Get for-sale ownerships
        ownerships = self.ownership_repo.get_drivers_for_sale_in_league(league_id)
        
        if not ownerships:
            logger.info("No drivers for sale in league %d", league_id)
            return []
        
        # Get driver records
        driver_ids = [o.driver_id for o in ownerships]
        drivers = self.drivers_repo.get_by_ids(driver_ids)
        
        if not drivers:
            logger.warning("No driver records found for for-sale drivers in league %d", league_id)
            return []
        
        # Get owner names
        owner_ids = [o.owner_id for o in ownerships if o.owner_id]
        owner_names = self.users_repo.get_users_names_by_ids(owner_ids)
        
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
            owner_names=owner_names,
            is_owned=True,
            is_owned_by_me=False,
            is_free_agent=False,
            is_for_sale=True,
            include_owner_names=True,
        )
        
        logger.info("Returning %d drivers for sale in league %d", len(enriched_drivers), league_id)
        return enriched_drivers
