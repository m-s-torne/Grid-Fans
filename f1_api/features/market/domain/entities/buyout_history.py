"""Buyout clause history domain entity"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class BuyoutHistory:
    """
    Pure domain entity for buyout clause history.
    
    Tracks when users activate buyout clauses against each other.
    Used to enforce business rules around buyout frequency limits.
    No SQLModel, no DB concerns - only business logic.
    
    Business rules:
    - Limited number of buyouts per season between same users
    - Buyout price is typically higher than market value
    - Creates transaction record in parallel
    """
    
    league_id: int
    buyer_id: int
    victim_id: int
    driver_id: int
    buyout_price: float
    season_year: int
    buyout_date: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None  # Assigned by persistence layer
    
    # Business methods - to be implemented in Phase 2
    
    def is_same_season(self, year: int) -> bool:
        """Check if buyout occurred in specified season"""
        return self.season_year == year
    
    def involves_users(self, buyer: int, victim: int) -> bool:
        """Check if buyout was between these two users"""
        return self.buyer_id == buyer and self.victim_id == victim
