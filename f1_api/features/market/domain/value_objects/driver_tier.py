"""Driver tier value object"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TierLevel(str, Enum):
    """Driver tier levels from highest to lowest"""
    S = "S"  # Elite tier - Championship contenders
    A = "A"  # Top tier - Regular podium finishers
    B = "B"  # Mid tier - Point scorers
    C = "C"  # Lower tier - Occasional points
    D = "D"  # Entry tier - Development drivers


@dataclass(frozen=True)
class DriverTier:
    """
    Immutable value object representing a driver's competitive tier.
    
    Tiers determine pricing, availability, and strategic value.
    Higher tiers have more restrictions and higher prices.
    """
    
    level: TierLevel
    
    def __post_init__(self):
        """Validate tier level"""
        if not isinstance(self.level, TierLevel):
            raise ValueError(f"Invalid tier level: {self.level}")
    
    @property
    def rank(self) -> int:
        """Get numeric rank (1=S, 5=D)"""
        ranks = {TierLevel.S: 1, TierLevel.A: 2, TierLevel.B: 3, TierLevel.C: 4, TierLevel.D: 5}
        return ranks[self.level]
    
    @property
    def base_price(self) -> float:
        """Get base price for this tier"""
        prices = {
            TierLevel.S: 15_000_000,
            TierLevel.A: 10_000_000,
            TierLevel.B: 5_000_000,
            TierLevel.C: 2_000_000,
            TierLevel.D: 500_000,
        }
        return prices[self.level]
    
    @property
    def max_per_team(self) -> Optional[int]:
        """Maximum number of drivers of this tier per team"""
        # S-tier drivers: max 2 per team (prevents stacking elite drivers)
        # A-tier drivers: max 2 per team
        # Others: unlimited
        limits = {
            TierLevel.S: 2,
            TierLevel.A: 2,
            TierLevel.B: None,
            TierLevel.C: None,
            TierLevel.D: None,
        }
        return limits[self.level]
    
    @property
    def lock_days_multiplier(self) -> float:
        """Lock period multiplier (higher tiers = longer locks)"""
        multipliers = {
            TierLevel.S: 1.5,  # 50% longer lock
            TierLevel.A: 1.25, # 25% longer lock
            TierLevel.B: 1.0,  # Standard lock
            TierLevel.C: 0.75, # 25% shorter lock
            TierLevel.D: 0.5,  # 50% shorter lock
        }
        return multipliers[self.level]
    
    def is_elite(self) -> bool:
        """Check if this is an elite tier (S or A)"""
        return self.level in (TierLevel.S, TierLevel.A)
    
    def is_higher_than(self, other: "DriverTier") -> bool:
        """Check if this tier is higher than another"""
        return self.rank < other.rank
    
    def is_lower_than(self, other: "DriverTier") -> bool:
        """Check if this tier is lower than another"""
        return self.rank > other.rank
    
    @classmethod
    def from_string(cls, tier_str: str) -> "DriverTier":
        """Create tier from string (case-insensitive)"""
        try:
            level = TierLevel(tier_str.upper())
            return cls(level)
        except ValueError:
            raise ValueError(f"Invalid tier string: {tier_str}. Must be S, A, B, C, or D")
    
    @classmethod
    def from_points(cls, total_points: float) -> "DriverTier":
        """
        Classify tier based on championship points.
        
        Args:
            total_points: Total championship points
            
        Returns:
            DriverTier based on points threshold
        """
        if total_points >= 200:
            return cls(TierLevel.S)
        elif total_points >= 100:
            return cls(TierLevel.A)
        elif total_points >= 50:
            return cls(TierLevel.B)
        elif total_points >= 10:
            return cls(TierLevel.C)
        else:
            return cls(TierLevel.D)
    
    def __str__(self) -> str:
        return self.level.value
    
    def __lt__(self, other: "DriverTier") -> bool:
        return self.rank < other.rank
    
    def __le__(self, other: "DriverTier") -> bool:
        return self.rank <= other.rank
    
    def __gt__(self, other: "DriverTier") -> bool:
        return self.rank > other.rank
    
    def __ge__(self, other: "DriverTier") -> bool:
        return self.rank >= other.rank
