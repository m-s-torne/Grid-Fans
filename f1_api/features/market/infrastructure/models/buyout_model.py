"""Buyout clause history SQLModel - Database table mapping"""
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime
from typing import Optional


class BuyoutClauseHistoryModel(SQLModel, table=True):
    """
    Buyout clause history database model (SQLModel).
    
    This is the persistence layer representation using SQLModel/SQLAlchemy.
    For business logic, see domain.entities.BuyoutHistory (pure dataclass).
    
    Tracks when users activate buyout clauses against each other.
    Used to enforce business rules around buyout frequency limits.
    
    Business rules:
    - Limited number of buyouts per season between same users
    - Buyout price is typically higher than market value
    - Creates transaction record in parallel
    """
    
    __tablename__ = "buyoutclausehistory"  # type: ignore[assignment]
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    league_id: int = SQLField(foreign_key="leagues.id")
    buyer_id: int = SQLField(
        foreign_key="users.id",
        description="User who activated buyout clause"
    )
    victim_id: int = SQLField(
        foreign_key="users.id",
        description="User whose driver was bought out"
    )
    driver_id: int = SQLField(foreign_key="drivers.id")
    buyout_price: float = SQLField(description="Price paid for buyout")
    buyout_date: datetime = SQLField(default_factory=datetime.now)
    season_year: int = SQLField(description="Season when buyout occurred")
    
    __table_args__ = {"extend_existing": True}
