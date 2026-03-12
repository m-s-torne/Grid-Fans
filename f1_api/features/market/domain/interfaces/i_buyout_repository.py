"""Buyout clause history repository interface"""
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from f1_api.features.market.domain.entities import BuyoutHistory


class IBuyoutRepository(Protocol):
    """
    Repository interface for buyout clause history operations.
    
    Uses Protocol for structural subtyping - no runtime overhead.
    Implementations must provide all methods defined here.
    """
    
    def create(self, buyout: "BuyoutHistory") -> "BuyoutHistory":
        """
        Create a new buyout clause history record.
        
        Args:
            buyout: BuyoutHistory entity to persist
            
        Returns:
            Created BuyoutHistory with ID assigned
        """
        ...
    
    def count_buyouts_between_users(
        self, 
        buyer_id: int, 
        victim_id: int, 
        league_id: int,
        season: int
    ) -> int:
        """
        Count how many times buyer has used buyout clause against victim.
        
        This is used to enforce business rules around buyout frequency limits.
        
        Args:
            buyer_id: User who initiated the buyouts
            victim_id: User whose driver was bought out
            league_id: League identifier
            season: Season year
            
        Returns:
            Count of buyout transactions matching the criteria
        """
        ...
