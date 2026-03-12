"""Buyout validator domain service"""
from typing import Tuple, Optional
from ..entities import DriverOwnership


class BuyoutValidator:
    """
    Domain service for validating buyout clause operations.
    
    Buyout clauses allow users to purchase drivers from other users
    at a premium price, bypassing the normal market listing.
    """
    
    # Business rule constants
    BUYOUT_MULTIPLIER = 1.3  # 130% of acquisition price
    MAX_BUYOUTS_PER_PAIR_PER_SEASON = 2  # Max buyouts between two users per season
    MIN_OWNERSHIP_DAYS_FOR_BUYOUT = 3  # Minimum days owned before buyout allowed
    
    @classmethod
    def validate_buyout(
        cls,
        ownership: DriverOwnership,
        buyer_id: int,
        victim_id: int,
        buyer_budget: float,
        previous_buyouts_count: int = 0,
    ) -> Tuple[bool, str, Optional[float]]:
        """
        Validate if buyout clause can be executed.
        
        Args:
            ownership: DriverOwnership entity
            buyer_id: User attempting to buy out
            victim_id: User being bought out from
            buyer_budget: Buyer's available budget
            previous_buyouts_count: Number of previous buyouts between these users
            
        Returns:
            Tuple of (is_valid, error_message, buyout_price)
            - is_valid: True if buyout can proceed
            - error_message: Error description if invalid, empty string if valid
            - buyout_price: Calculated buyout price if valid, None if invalid
        """
        # Rule 1: Driver must be owned by someone
        if ownership.is_free_agent():
            return False, "Cannot buyout a free agent. Purchase from market instead.", None
        
        # Rule 2: Cannot buyout your own driver
        if ownership.is_owned_by(buyer_id):
            return False, "Cannot buyout your own driver.", None
        
        # Rule 3: Must buyout from correct owner
        if ownership.owner_id != victim_id:
            return False, "Driver is not owned by specified user.", None
        
        # Rule 4: Driver must not be locked
        if ownership.is_locked():
            days_left = ownership.days_until_unlock
            return False, f"Driver is locked for {days_left} more day(s).", None
        
        # Rule 5: Driver must not be listed for sale (use normal purchase instead)
        if ownership.is_listed_for_sale:
            return False, "Driver is listed for sale. Purchase normally instead of buyout.", None
        
        # Rule 6: Check buyout frequency limit
        if previous_buyouts_count >= cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON:
            return (
                False,
                f"Maximum {cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON} buyouts per season between users reached.",
                None,
            )
        
        # Calculate buyout price
        buyout_price = cls.calculate_buyout_price(ownership.acquisition_price)
        
        # Rule 7: Buyer must have sufficient budget
        if buyer_budget < buyout_price:
            return (
                False,
                f"Insufficient budget. Need ${buyout_price:,.0f}, have ${buyer_budget:,.0f}.",
                None,
            )
        
        # All validations passed
        return True, "", buyout_price
    
    @classmethod
    def calculate_buyout_price(cls, acquisition_price: float) -> float:
        """
        Calculate buyout clause price.
        
        Args:
            acquisition_price: Price at which driver was acquired
            
        Returns:
            Buyout price (130% of acquisition)
        """
        return acquisition_price * cls.BUYOUT_MULTIPLIER
    
    @classmethod
    def estimate_buyout_value(
        cls,
        ownership: DriverOwnership,
    ) -> Optional[float]:
        """
        Estimate buyout value for a driver.
        
        Args:
            ownership: DriverOwnership entity
            
        Returns:
            Estimated buyout price, None if not eligible
        """
        if ownership.is_free_agent():
            return None
        
        if ownership.is_locked():
            return None
        
        return cls.calculate_buyout_price(ownership.acquisition_price)
    
    @classmethod
    def check_anti_abuse(
        cls,
        _buyer_id: int,
        _victim_id: int,
        buyouts_in_season: int,
    ) -> Tuple[bool, str]:
        """
        Check for potential abuse of buyout system.
        
        Args:
            buyer_id: User attempting buyout
            victim_id: User being bought out from
            buyouts_in_season: Total buyouts between these users this season
            
        Returns:
            Tuple of (is_allowed, message)
        """
        # Prevent same users from repeatedly buying out from each other
        if buyouts_in_season >= cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON:
            return (
                False,
                f"Buyout limit reached between these users this season "
                f"({cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON} maximum).",
            )
        
        # Warning at half the limit
        if buyouts_in_season >= cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON / 2:
            return (
                True,
                f"Warning: {buyouts_in_season} of {cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON} "
                f"buyouts used between these users this season.",
            )
        
        return True, ""
    
    @classmethod
    def get_remaining_buyouts(
        cls,
        current_buyouts: int,
    ) -> int:
        """
        Get number of remaining buyouts allowed.
        
        Args:
            current_buyouts: Number of buyouts already used
            
        Returns:
            Number of buyouts remaining
        """
        return max(0, cls.MAX_BUYOUTS_PER_PAIR_PER_SEASON - current_buyouts)
