"""Driver ownership repository interface"""
from typing import Protocol, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from f1_api.features.market.domain.entities import DriverOwnership


class IOwnershipRepository(Protocol):
    """
    Repository interface for driver ownership operations.
    
    Uses Protocol for structural subtyping - no runtime overhead.
    Implementations must provide all methods defined here.
    """
    
    def get_by_driver_and_league(
        self, 
        driver_id: int, 
        league_id: int
    ) -> Optional["DriverOwnership"]:
        """
        Get ownership record for a specific driver in a league.
        
        Args:
            driver_id: Driver identifier
            league_id: League identifier
            
        Returns:
            DriverOwnership if found, None otherwise
        """
        ...
    
    def get_free_drivers_in_league(
        self, 
        league_id: int
    ) -> list["DriverOwnership"]:
        """
        Get all drivers without owners in a league (free agents).
        
        Args:
            league_id: League identifier
            
        Returns:
            List of driver ownerships where owner_id is None
        """
        ...
    
    def get_drivers_for_sale_in_league(
        self, 
        league_id: int
    ) -> list["DriverOwnership"]:
        """
        Get all drivers listed for sale in a league.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of driver ownerships where is_listed_for_sale is True
        """
        ...
    
    def get_owned_by_user_in_league(
        self, 
        user_id: int, 
        league_id: int
    ) -> list["DriverOwnership"]:
        """
        Get all drivers owned by a specific user in a league.
        
        Args:
            user_id: User identifier
            league_id: League identifier
            
        Returns:
            List of driver ownerships belonging to the user
        """
        ...
    
    def update(self, ownership: "DriverOwnership") -> "DriverOwnership":
        """
        Update an existing driver ownership record.
        
        Args:
            ownership: DriverOwnership entity to update
            
        Returns:
            Updated DriverOwnership entity
        """
        ...

    def create(self, ownership: "DriverOwnership") -> "DriverOwnership":
        """
        Create a new driver ownership record.

        Args:
            ownership: DriverOwnership entity to persist

        Returns:
            Created DriverOwnership entity
        """
        ...
