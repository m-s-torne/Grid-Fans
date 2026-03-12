"""Driver ownership SQLModel - Database table mapping"""
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import UniqueConstraint


class DriverOwnershipModel(SQLModel, table=True):
    """
    Driver ownership database model (SQLModel).
    
    This is the persistence layer representation using SQLModel/SQLAlchemy.
    For business logic, see domain.entities.DriverOwnership (pure dataclass).
    
    Invariants:
    - A driver can only have one owner per league (None = free agent)
    - If listed for sale, must have asking_price
    - If locked, locked_until must be in the future
    - acquisition_price is immutable after purchase (business rule)
    """
    
    __tablename__ = "driverownership"  # type: ignore[assignment]
    
    driver_id: int = SQLField(foreign_key="drivers.id", primary_key=True)
    league_id: int = SQLField(foreign_key="leagues.id", primary_key=True)
    
    owner_id: Optional[int] = SQLField(
        foreign_key="users.id",
        default=None,
        description="User who owns this driver (None = free agent)"
    )
    
    is_listed_for_sale: bool = SQLField(
        default=False,
        description="Whether driver is currently listed for sale"
    )
    
    acquisition_price: float = SQLField(
        description="Price paid when acquired - IMMUTABLE during listing"
    )
    
    asking_price: Optional[float] = SQLField(
        default=None,
        description="Selling price when listed for sale"
    )
    
    locked_until: Optional[datetime] = SQLField(
        default=None,
        description="Lock expiration timestamp"
    )
    
    created_at: datetime = SQLField(default_factory=datetime.now)
    updated_at: datetime = SQLField(default_factory=datetime.now)
    
    __table_args__ = (
        UniqueConstraint(
            'driver_id',
            'league_id',
            name='unique_driver_league_ownership'
        ),
        {"extend_existing": True}
    )
    
    # Domain logic methods (for backward compatibility - to be moved to domain layer)
    
    def is_free_agent(self) -> bool:
        """Check if driver is a free agent (no owner)"""
        return self.owner_id is None
    
    def is_owned_by(self, user_id: int) -> bool:
        """Check if driver is owned by specific user"""
        return self.owner_id == user_id
    
    def is_locked(self) -> bool:
        """Check if driver is locked"""
        if self.locked_until is None:
            return False
        return self.locked_until > datetime.now()
    
    def can_be_sold(self) -> tuple[bool, str]:
        """Check if driver can be sold"""
        if self.is_free_agent():
            return False, "Driver is already a free agent"
        
        if self.is_locked() and self.locked_until is not None:
            return False, f"Driver is locked until {self.locked_until.isoformat()}"
        
        return True, ""
    
    def can_be_listed(self) -> tuple[bool, str]:
        """Check if driver can be listed for sale"""
        can_sell, reason = self.can_be_sold()
        if not can_sell:
            return False, reason
        if self.is_listed_for_sale:
            return False, "Driver is already listed for sale"
        
        return True, ""
    
    def can_be_purchased(self) -> tuple[bool, str]:
        """Check if driver can be purchased"""
        if not self.is_free_agent():
            return False, "Driver is not a free agent"
        
        return True, ""
    
    def assign_to_user(
        self,
        user_id: int,
        price: float,
        lock_days: int = 7
    ) -> None:
        """Assign driver to a user (purchase from market)"""
        can_purchase, reason = self.can_be_purchased()
        if not can_purchase:
            raise ValueError(reason)
        
        self.owner_id = user_id
        self.acquisition_price = price
        self.locked_until = datetime.now() + timedelta(days=lock_days)
        self.is_listed_for_sale = False
        self.asking_price = None
        self.updated_at = datetime.now()
    
    def transfer_to_user(
        self,
        new_owner_id: int,
        current_market_price: float,
        lock_days: int = 7
    ) -> None:
        """Transfer driver to new owner (purchase from another user)"""
        if not self.is_listed_for_sale:
            raise ValueError("Driver is not listed for sale")
        
        self.owner_id = new_owner_id
        self.acquisition_price = current_market_price
        self.asking_price = None
        self.locked_until = datetime.now() + timedelta(days=lock_days)
        self.is_listed_for_sale = False
        self.updated_at = datetime.now()
    
    def release_to_market(self) -> None:
        """Release driver back to market (sell or release)"""
        can_sell, reason = self.can_be_sold()
        if not can_sell:
            raise ValueError(reason)
        
        self.owner_id = None
        self.is_listed_for_sale = False
        self.asking_price = None
        self.locked_until = None
        self.updated_at = datetime.now()
    
    def list_for_sale(self, asking_price: Optional[float] = None) -> None:
        """List driver for sale"""
        can_list, reason = self.can_be_listed()
        if not can_list:
            raise ValueError(reason)
        
        self.is_listed_for_sale = True
        self.asking_price = asking_price or self.acquisition_price
        self.updated_at = datetime.now()
    
    def unlist_from_sale(self) -> None:
        """Remove driver from sale listings"""
        self.is_listed_for_sale = False
        self.asking_price = None
        self.updated_at = datetime.now()
    
    def apply_lock(self, days: int) -> None:
        """Apply a lock for specified number of days"""
        self.locked_until = datetime.now() + timedelta(days=days)
        self.updated_at = datetime.now()
    
    def remove_lock(self) -> None:
        """Remove lock from driver"""
        self.locked_until = None
        self.updated_at = datetime.now()
    
    @property
    def potential_profit(self) -> Optional[float]:
        """Calculate potential profit if sold at asking price"""
        if not self.is_listed_for_sale or self.asking_price is None:
            return None
        
        return self.asking_price - self.acquisition_price
    
    @property
    def days_until_unlock(self) -> Optional[int]:
        """Calculate days remaining until unlock"""
        if not self.is_locked() or self.locked_until is None:
            return None
        
        delta = self.locked_until - datetime.now()
        return max(0, delta.days)
