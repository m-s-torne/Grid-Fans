"""Use case: Get market statistics and analytics"""
from typing import List, Dict

from f1_api.features.market.domain.entities import DriverOwnership
from f1_api.features.market.domain.interfaces import (
    IOwnershipRepository,
    ITransactionRepository,
)


class GetMarketStatsUseCase:
    """
    Use case for retrieving market statistics and analytics.
    
    Provides:
    - Current market listings (drivers for sale)
    - Free agents available
    - Recent transaction activity
    - Price distribution and trends
    - Market health indicators
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transaction_repo: ITransactionRepository,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            transaction_repo: Repository for transaction operations
        """
        self.ownership_repo = ownership_repo
        self.transaction_repo = transaction_repo
    
    def get_market_listings(self, league_id: int) -> List[DriverOwnership]:
        """
        Get all drivers currently listed for sale.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of driver ownerships for sale
        """
        return self.ownership_repo.get_drivers_for_sale_in_league(league_id)
    
    def get_free_agents(self, league_id: int) -> List[DriverOwnership]:
        """
        Get all free agents (drivers without owners).
        
        Args:
            league_id: League identifier
            
        Returns:
            List of free agent driver ownerships
        """
        return self.ownership_repo.get_free_drivers_in_league(league_id)
    
    def get_user_drivers(
        self, user_id: int, league_id: int
    ) -> List[DriverOwnership]:
        """
        Get all drivers owned by a specific user.
        
        Args:
            user_id: User identifier
            league_id: League identifier
            
        Returns:
            List of driver ownerships for the user
        """
        return self.ownership_repo.get_owned_by_user_in_league(user_id, league_id)
    
    def get_market_stats(self, league_id: int) -> Dict:
        """
        Get comprehensive market statistics.
        
        Args:
            league_id: League identifier
            
        Returns:
            Dictionary with market statistics
        """
        # Get all transactions
        transactions = self.transaction_repo.get_by_league(league_id)
        
        # Get market listings
        listings = self.ownership_repo.get_drivers_for_sale_in_league(league_id)
        
        # Get free agents
        free_agents = self.ownership_repo.get_free_drivers_in_league(league_id)
        
        # Calculate statistics
        total_transactions = len(transactions)
        
        if transactions:
            total_volume = sum(t.transaction_price for t in transactions)
            avg_price = total_volume / total_transactions if total_transactions > 0 else 0
            highest_price = max(t.transaction_price for t in transactions)
        else:
            total_volume = 0
            avg_price = 0
            highest_price = 0
        
        # Count transaction types
        transaction_types: Dict[str, int] = {}
        for t in transactions:
            transaction_types[t.transaction_type] = (
                transaction_types.get(t.transaction_type, 0) + 1
            )
        
        # Calculate price tiers distribution
        tier_distribution = self._calculate_tier_distribution(listings)
        
        return {
            "league_id": league_id,
            "total_transactions": total_transactions,
            "total_volume": total_volume,
            "average_price": avg_price,
            "highest_price": highest_price,
            "drivers_for_sale": len(listings),
            "free_agents": len(free_agents),
            "transaction_types": transaction_types,
            "tier_distribution": tier_distribution,
        }
    
    def _calculate_tier_distribution(
        self, listings: List[DriverOwnership]
    ) -> Dict[str, int]:
        """
        Calculate price tier distribution for market listings.
        
        Args:
            listings: List of driver ownerships for sale
            
        Returns:
            Dictionary mapping tier names to counts
        """
        distribution: Dict[str, int] = {
            "budget": 0,  # < 5M
            "mid": 0,  # 5M - 15M
            "premium": 0,  # 15M - 30M
            "elite": 0,  # > 30M
        }
        
        for ownership in listings:
            if ownership.asking_price is None:
                continue
            
            if ownership.asking_price < 5_000_000:
                distribution["budget"] += 1
            elif ownership.asking_price < 15_000_000:
                distribution["mid"] += 1
            elif ownership.asking_price < 30_000_000:
                distribution["premium"] += 1
            else:
                distribution["elite"] += 1
        
        return distribution
