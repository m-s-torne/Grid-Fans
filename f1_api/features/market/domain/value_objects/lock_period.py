"""Lock period value object"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional


@dataclass(frozen=True)
class LockPeriod:
    """
    Immutable value object representing a driver lock period.
    
    Drivers are locked after purchase/transfer to prevent rapid trading.
    Lock prevents listing for sale or transferring the driver.
    """
    
    days: int
    
    # Lock duration constants
    DEFAULT_LOCK_DAYS: int = 7
    MIN_LOCK_DAYS: int = 1
    MAX_LOCK_DAYS: int = 30
    EMERGENCY_LOCK_DAYS: int = 3  # Shorter lock for emergency assignments
    
    def __post_init__(self):
        """Validate lock period"""
        if self.days < self.MIN_LOCK_DAYS:
            raise ValueError(f"Lock period cannot be less than {self.MIN_LOCK_DAYS} day(s)")
        if self.days > self.MAX_LOCK_DAYS:
            raise ValueError(f"Lock period cannot exceed {self.MAX_LOCK_DAYS} days")
    
    def calculate_unlock_date(self, start_date: Optional[datetime] = None) -> datetime:
        """
        Calculate when the lock expires.
        
        Args:
            start_date: When lock started (defaults to now)
            
        Returns:
            Datetime when lock expires
        """
        if start_date is None:
            start_date = datetime.now()
        
        return start_date + timedelta(days=self.days)
    
    def is_expired(self, lock_until: datetime) -> bool:
        """
        Check if a lock has expired.
        
        Args:
            lock_until: The expiration datetime
            
        Returns:
            True if lock has expired
        """
        return datetime.now() >= lock_until
    
    def days_remaining(self, lock_until: datetime) -> int:
        """
        Calculate days remaining in lock period.
        
        Args:
            lock_until: The expiration datetime
            
        Returns:
            Number of days remaining (0 if expired)
        """
        if self.is_expired(lock_until):
            return 0
        
        delta = lock_until - datetime.now()
        return max(0, delta.days)
    
    def hours_remaining(self, lock_until: datetime) -> int:
        """
        Calculate hours remaining in lock period.
        
        Args:
            lock_until: The expiration datetime
            
        Returns:
            Number of hours remaining (0 if expired)
        """
        if self.is_expired(lock_until):
            return 0
        
        delta = lock_until - datetime.now()
        return max(0, int(delta.total_seconds() / 3600))
    
    def with_multiplier(self, multiplier: float) -> "LockPeriod":
        """
        Apply a multiplier to the lock period.
        
        Args:
            multiplier: Multiplier to apply (e.g., 1.5 for 50% longer)
            
        Returns:
            New LockPeriod with adjusted duration
            
        Example:
            >>> lock = LockPeriod(7)
            >>> extended = lock.with_multiplier(1.5)
            >>> extended.days
            10  # 7 * 1.5 = 10.5, rounded down
        """
        if multiplier <= 0:
            raise ValueError("Multiplier must be positive")
        
        new_days = int(self.days * multiplier)
        # Ensure within bounds
        new_days = max(self.MIN_LOCK_DAYS, min(new_days, self.MAX_LOCK_DAYS))
        return LockPeriod(new_days)
    
    def extend_by(self, additional_days: int) -> "LockPeriod":
        """
        Extend lock period by additional days.
        
        Args:
            additional_days: Days to add
            
        Returns:
            New LockPeriod with extended duration
        """
        new_days = min(self.days + additional_days, self.MAX_LOCK_DAYS)
        return LockPeriod(new_days)
    
    def reduce_by(self, fewer_days: int) -> "LockPeriod":
        """
        Reduce lock period by specified days.
        
        Args:
            fewer_days: Days to subtract
            
        Returns:
            New LockPeriod with reduced duration
        """
        new_days = max(self.days - fewer_days, self.MIN_LOCK_DAYS)
        return LockPeriod(new_days)
    
    @classmethod
    def default(cls) -> "LockPeriod":
        """Create default lock period (7 days)"""
        return cls(cls.DEFAULT_LOCK_DAYS)
    
    @classmethod
    def emergency(cls) -> "LockPeriod":
        """Create emergency lock period (3 days)"""
        return cls(cls.EMERGENCY_LOCK_DAYS)
    
    @classmethod
    def none(cls) -> "LockPeriod":
        """Create minimal lock period (1 day)"""
        return cls(cls.MIN_LOCK_DAYS)
    
    def __str__(self) -> str:
        if self.days == 1:
            return "1 day"
        return f"{self.days} days"
    
    def __repr__(self) -> str:
        return f"LockPeriod({self.days})"
    
    def __lt__(self, other: "LockPeriod") -> bool:
        return self.days < other.days
    
    def __le__(self, other: "LockPeriod") -> bool:
        return self.days <= other.days
    
    def __gt__(self, other: "LockPeriod") -> bool:
        return self.days > other.days
    
    def __ge__(self, other: "LockPeriod") -> bool:
        return self.days >= other.days
