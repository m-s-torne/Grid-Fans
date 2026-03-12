"""Driver price value object"""
from dataclasses import dataclass


@dataclass(frozen=True)
class DriverPrice:
    """
    Immutable value object representing a driver's market price.
    
    Prices are always in currency units (e.g., 1_000_000 = $1M).
    Validation ensures prices stay within reasonable bounds.
    """
    
    amount: float
    
    # Price constraints
    MIN_PRICE: float = 100_000  # $100K minimum
    MAX_PRICE: float = 100_000_000  # $100M maximum
    
    def __post_init__(self):
        """Validate price constraints"""
        if self.amount < 0:
            raise ValueError("Price cannot be negative")
        if self.amount < self.MIN_PRICE:
            raise ValueError(f"Price cannot be less than {self.MIN_PRICE:,.0f}")
        if self.amount > self.MAX_PRICE:
            raise ValueError(f"Price cannot exceed {self.MAX_PRICE:,.0f}")
    
    def apply_discount(self, percentage: float) -> "DriverPrice":
        """
        Apply a discount percentage and return new price.
        
        Args:
            percentage: Discount as decimal (0.2 = 20% off)
            
        Returns:
            New DriverPrice with discount applied
            
        Example:
            >>> price = DriverPrice(1_000_000)
            >>> discounted = price.apply_discount(0.2)  # 20% off
            >>> discounted.amount
            800_000.0
        """
        if not 0 <= percentage <= 1:
            raise ValueError("Discount percentage must be between 0 and 1")
        
        new_amount = self.amount * (1 - percentage)
        return DriverPrice(max(new_amount, self.MIN_PRICE))
    
    def apply_markup(self, percentage: float) -> "DriverPrice":
        """
        Apply a markup percentage and return new price.
        
        Args:
            percentage: Markup as decimal (0.3 = 30% markup)
            
        Returns:
            New DriverPrice with markup applied
            
        Example:
            >>> price = DriverPrice(1_000_000)
            >>> marked_up = price.apply_markup(0.3)  # 30% markup
            >>> marked_up.amount
            1_300_000.0
        """
        if percentage < 0:
            raise ValueError("Markup percentage cannot be negative")
        
        new_amount = self.amount * (1 + percentage)
        return DriverPrice(min(new_amount, self.MAX_PRICE))
    
    def difference_from(self, other: "DriverPrice") -> float:
        """
        Calculate price difference from another price.
        
        Returns:
            Positive if this price is higher, negative if lower
        """
        return self.amount - other.amount
    
    def percentage_of(self, other: "DriverPrice") -> float:
        """
        Calculate this price as percentage of another price.
        
        Returns:
            Percentage (1.0 = 100%)
        """
        if other.amount == 0:
            return 0.0
        return self.amount / other.amount
    
    @classmethod
    def from_tier(cls, tier: str, base_multiplier: float = 1.0) -> "DriverPrice":
        """
        Create price based on driver tier.
        
        Args:
            tier: Driver tier (S, A, B, C, D)
            base_multiplier: Additional multiplier for dynamic pricing
            
        Returns:
            DriverPrice based on tier
        """
        tier_prices = {
            "S": 15_000_000,  # $15M
            "A": 10_000_000,  # $10M
            "B": 5_000_000,   # $5M
            "C": 2_000_000,   # $2M
            "D": 500_000,     # $500K
        }
        
        base_price = tier_prices.get(tier.upper(), 1_000_000)
        return cls(base_price * base_multiplier)
    
    def __str__(self) -> str:
        """Format price as currency string"""
        if self.amount >= 1_000_000:
            return f"${self.amount / 1_000_000:.1f}M"
        elif self.amount >= 1_000:
            return f"${self.amount / 1_000:.0f}K"
        else:
            return f"${self.amount:.0f}"
    
    def __lt__(self, other: "DriverPrice") -> bool:
        return self.amount < other.amount
    
    def __le__(self, other: "DriverPrice") -> bool:
        return self.amount <= other.amount
    
    def __gt__(self, other: "DriverPrice") -> bool:
        return self.amount > other.amount
    
    def __ge__(self, other: "DriverPrice") -> bool:
        return self.amount >= other.amount
