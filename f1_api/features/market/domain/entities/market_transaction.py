"""Market transaction domain entity"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class MarketTransaction:
    """
    Pure domain entity for market transactions.
    
    Records all market activity for audit trail and analytics.
    No SQLModel, no DB concerns - only business logic.
    
    Transaction types:
    - 'buy_from_market': User purchases free agent
    - 'buy_from_user': User purchases from another user
    - 'sell_to_market': User releases driver to market
    - 'buyout_clause': User activates buyout clause
    - 'emergency_assignment': Admin assigns driver
    """
    
    driver_id: int
    league_id: int
    buyer_id: int
    transaction_price: float
    transaction_type: str
    seller_id: Optional[int] = None  # None = purchase from free market
    transaction_date: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None  # Assigned by persistence layer
    
    # Business methods - to be implemented in Phase 2
    
    def is_free_market_purchase(self) -> bool:
        """Check if this was a purchase from free market"""
        return self.transaction_type == "buy_from_market" and self.seller_id is None
    
    def is_user_to_user_transaction(self) -> bool:
        """Check if this was a transaction between users"""
        return self.seller_id is not None and self.transaction_type == "buy_from_user"
    
    def is_buyout(self) -> bool:
        """Check if this was a buyout clause activation"""
        return self.transaction_type == "buyout_clause"
    
    def involves_user(self, user_id: int) -> bool:
        """Check if user was involved in this transaction (buyer or seller)"""
        return self.buyer_id == user_id or self.seller_id == user_id
