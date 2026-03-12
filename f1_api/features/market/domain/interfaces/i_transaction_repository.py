"""Market transaction repository interface"""
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from f1_api.features.market.domain.entities import MarketTransaction


class ITransactionRepository(Protocol):
    """
    Repository interface for market transaction operations.
    
    Uses Protocol for structural subtyping - no runtime overhead.
    Implementations must provide all methods defined here.
    """
    
    def create(self, transaction: "MarketTransaction") -> "MarketTransaction":
        """
        Create a new market transaction record.
        
        Args:
            transaction: MarketTransaction entity to persist
            
        Returns:
            Created MarketTransaction with ID assigned
        """
        ...
    
    def get_by_league(self, league_id: int) -> list["MarketTransaction"]:
        """
        Get all market transactions for a specific league.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of all transactions in the league, ordered by date descending
        """
        ...
