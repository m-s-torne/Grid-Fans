"""Market transaction SQLModel - Database table mapping"""
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime
from typing import Optional


class MarketTransactionModel(SQLModel, table=True):
    """
    Market transaction database model (SQLModel).
    
    This is the persistence layer representation using SQLModel/SQLAlchemy.
    For business logic, see domain.entities.MarketTransaction (pure dataclass).
    
    Records all market activity for audit trail and analytics.
    
    Transaction types:
    - 'buy_from_market': User purchases free agent
    - 'buy_from_user': User purchases from another user
    - 'sell_to_market': User releases driver to market
    - 'buyout_clause': User activates buyout clause
    - 'emergency_assignment': Admin assigns driver
    """
    
    __tablename__ = "markettransactions"  # type: ignore[assignment]
    
    id: Optional[int] = SQLField(default=None, primary_key=True)
    driver_id: int = SQLField(foreign_key="drivers.id")
    league_id: int = SQLField(foreign_key="leagues.id")
    seller_id: Optional[int] = SQLField(
        foreign_key="users.id", 
        default=None,
        description="User who sold driver (None = free market purchase)"
    )
    buyer_id: int = SQLField(
        foreign_key="users.id",
        description="User who purchased driver"
    )
    transaction_price: float = SQLField(description="Price of the transaction")
    transaction_type: str = SQLField(description="Type of market transaction")
    transaction_date: datetime = SQLField(default_factory=datetime.now)
    
    __table_args__ = {"extend_existing": True}
