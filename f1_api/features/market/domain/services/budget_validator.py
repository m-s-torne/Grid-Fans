"""Budget validator domain service"""
from typing import Tuple, List, Dict, Any


class BudgetValidator:
    """
    Domain service for validating budget constraints.
    
    Ensures users have sufficient funds for purchases and maintains
    minimum budget requirements for team viability.
    """
    
    # Budget constants (in currency units)
    STARTING_BUDGET = 100_000_000  # $100M starting budget
    MINIMUM_RESERVE_BUDGET = 5_000_000  # $5M minimum reserve
    EMERGENCY_BUDGET_THRESHOLD = 1_000_000  # $1M emergency threshold
    
    @classmethod
    def validate_purchase(
        cls,
        current_budget: float,
        purchase_price: float,
        maintain_reserve: bool = True,
    ) -> Tuple[bool, str]:
        """
        Validate if user has sufficient budget for purchase.
        
        Args:
            current_budget: User's current available budget
            purchase_price: Price of item to purchase
            maintain_reserve: Whether to enforce minimum reserve
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Basic validation
        if purchase_price < 0:
            return False, "Purchase price cannot be negative."
        
        if current_budget < 0:
            return False, "Current budget cannot be negative."
        
        # Check if sufficient funds
        if purchase_price > current_budget:
            shortage = purchase_price - current_budget
            return (
                False,
                f"Insufficient budget. Need ${purchase_price:,.0f}, "
                f"have ${current_budget:,.0f}. Short by ${shortage:,.0f}.",
            )
        
        # Check if reserve will be maintained
        if maintain_reserve:
            budget_after_purchase = current_budget - purchase_price
            
            if budget_after_purchase < cls.MINIMUM_RESERVE_BUDGET:
                return (
                    False,
                    f"Purchase would leave ${budget_after_purchase:,.0f}, "
                    f"below minimum reserve of ${cls.MINIMUM_RESERVE_BUDGET:,.0f}.",
                )
        
        return True, ""
    
    @classmethod
    def calculate_remaining_budget(
        cls,
        current_budget: float,
        purchase_price: float,
    ) -> float:
        """
        Calculate budget remaining after purchase.
        
        Args:
            current_budget: Current available budget
            purchase_price: Price of purchase
            
        Returns:
            Budget remaining after purchase
        """
        return max(0, current_budget - purchase_price)
    
    @classmethod
    def calculate_max_affordable_price(
        cls,
        current_budget: float,
        maintain_reserve: bool = True,
    ) -> float:
        """
        Calculate maximum affordable purchase price.
        
        Args:
            current_budget: Current available budget
            maintain_reserve: Whether to maintain minimum reserve
            
        Returns:
            Maximum price user can afford
        """
        if maintain_reserve:
            return max(0, current_budget - cls.MINIMUM_RESERVE_BUDGET)
        
        return current_budget
    
    @classmethod
    def check_budget_health(
        cls,
        current_budget: float,
    ) -> Dict[str, Any]:
        """
        Assess overall budget health and status.
        
        Args:
            current_budget: Current available budget
            
        Returns:
            Dictionary with budget health metrics
        """
        health = {
            "current_budget": current_budget,
            "starting_budget": cls.STARTING_BUDGET,
            "minimum_reserve": cls.MINIMUM_RESERVE_BUDGET,
            "emergency_threshold": cls.EMERGENCY_BUDGET_THRESHOLD,
        }
        
        # Calculate percentage of starting budget
        budget_percentage = (current_budget / cls.STARTING_BUDGET) * 100
        health["budget_percentage"] = round(budget_percentage, 2)
        
        # Determine budget status
        if current_budget < cls.EMERGENCY_BUDGET_THRESHOLD:
            health["status"] = "critical"
            health["status_message"] = "Budget critically low. Consider selling drivers."
        elif current_budget < cls.MINIMUM_RESERVE_BUDGET:
            health["status"] = "warning"
            health["status_message"] = "Budget below recommended reserve."
        elif current_budget < cls.STARTING_BUDGET * 0.25:
            health["status"] = "low"
            health["status_message"] = "Budget running low."
        elif current_budget < cls.STARTING_BUDGET * 0.50:
            health["status"] = "moderate"
            health["status_message"] = "Budget at moderate level."
        else:
            health["status"] = "healthy"
            health["status_message"] = "Budget in good condition."
        
        # Calculate purchasing power
        health["max_affordable"] = cls.calculate_max_affordable_price(current_budget)
        
        return health
    
    @classmethod
    def validate_batch_purchases(
        cls,
        current_budget: float,
        purchase_prices: List[float],
    ) -> Tuple[bool, str, List[bool]]:
        """
        Validate multiple purchases in sequence.
        
        Args:
            current_budget: Starting budget
            purchase_prices: List of purchase prices in order
            
        Returns:
            Tuple of (all_valid, error_message, individual_validations)
        """
        remaining_budget = current_budget
        validations = []
        
        for i, price in enumerate(purchase_prices, 1):
            is_valid, error_msg = cls.validate_purchase(
                remaining_budget,
                price,
                maintain_reserve=(i == len(purchase_prices)),  # Only check reserve on last purchase
            )
            
            validations.append(is_valid)
            
            if not is_valid:
                return False, f"Purchase {i} failed: {error_msg}", validations
            
            remaining_budget -= price
        
        return True, "", validations
    
    @classmethod
    def suggest_budget_actions(
        cls,
        current_budget: float,
        desired_purchase_price: float,
    ) -> List[str]:
        """
        Suggest actions to afford a desired purchase.
        
        Args:
            current_budget: Current available budget
            desired_purchase_price: Price of desired purchase
            
        Returns:
            List of suggested actions
        """
        suggestions = []
        
        shortage = desired_purchase_price - current_budget
        
        if shortage <= 0:
            suggestions.append("You can afford this purchase!")
            return suggestions
        
        suggestions.append(f"You need an additional ${shortage:,.0f}.")
        suggestions.append(f"Consider selling drivers worth at least ${shortage:,.0f}.")
        
        # Calculate how many drivers of different tiers would cover shortage
        tier_prices = {
            "S-tier": 15_000_000,
            "A-tier": 10_000_000,
            "B-tier": 5_000_000,
            "C-tier": 2_000_000,
        }
        
        for tier, price in tier_prices.items():
            drivers_needed = int(shortage / price) + 1
            if drivers_needed == 1:
                suggestions.append(f"Selling 1 {tier} driver would cover the shortage.")
            elif drivers_needed <= 3:
                suggestions.append(f"Selling {drivers_needed} {tier} drivers would cover the shortage.")
        
        return suggestions
