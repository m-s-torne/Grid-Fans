"""
User Teams Domain Layer - Domain Services
Pure business logic services without infrastructure dependencies
"""
import logging
from sqlmodel import Session, select
from fastapi import HTTPException

from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.teams.domain.models import Teams
from f1_api.core.f1_data.domain.models import SessionResult

logger = logging.getLogger(__name__)


class DriverPricingService:
    """
    Domain service for calculating driver prices based on performance
    Formula: 10M + (points × 10k) + (podiums × 50k) + (victories × 100k)
    """
    
    BASE_PRICE = 10_000_000
    POINTS_MULTIPLIER = 10_000
    PODIUM_BONUS = 50_000
    VICTORY_BONUS = 100_000
    
    def __init__(self, session: Session):
        self.session = session
    
    def calculate_price(self, driver_id: int) -> int:
        """
        Calculate driver price based on season performance
        
        Args:
            driver_id: ID of the driver
            
        Returns:
            int: Calculated price for the driver (no rounding for max precision)
        """
        # Get driver's season results
        results = self.session.exec(
            select(SessionResult).where(SessionResult.driver_id == driver_id)
        ).all()
        
        # Calculate stats
        total_points = 0
        podiums = 0
        victories = 0
        
        for result in results:
            if result.points:
                total_points += result.points
            
            # Race session (session_number == 5)
            if result.session_number == 5:
                if result.position == "1":
                    victories += 1
                    podiums += 1
                elif result.position in ["2", "3"]:
                    podiums += 1
        
        # Calculate price using unified formula
        price = (
            self.BASE_PRICE + 
            (int(total_points) * self.POINTS_MULTIPLIER) + 
            (podiums * self.PODIUM_BONUS) + 
            (victories * self.VICTORY_BONUS)
        )
        
        logger.debug(f"Driver {driver_id} price: ${price / 1_000_000:.1f}M (points={total_points}, podiums={podiums}, victories={victories})")
        
        return price


class BudgetCalculationService:
    """
    Domain service for calculating team budgets
    """
    
    INITIAL_BUDGET = 100_000_000  # 100M initial budget
    
    def __init__(self, session: Session, pricing_service: DriverPricingService):
        self.session = session
        self.pricing_service = pricing_service
    
    def calculate_remaining_budget(
        self, 
        driver_1_id: int, 
        driver_2_id: int, 
        driver_3_id: int, 
        constructor_id: int
    ) -> int:
        """
        Calculate remaining budget based on selected drivers and constructor prices
        
        Args:
            driver_1_id: ID of first driver
            driver_2_id: ID of second driver
            driver_3_id: ID of third driver
            constructor_id: ID of constructor
            
        Returns:
            int: Remaining budget after purchasing drivers and constructor
            
        Raises:
            HTTPException: If any driver or constructor not found, or budget exceeded
        """
        # Get drivers
        driver_1 = self.session.exec(select(Drivers).where(Drivers.id == driver_1_id)).first()
        driver_2 = self.session.exec(select(Drivers).where(Drivers.id == driver_2_id)).first()
        driver_3 = self.session.exec(select(Drivers).where(Drivers.id == driver_3_id)).first()
        
        drivers = [driver_1, driver_2, driver_3]
        
        if not all(drivers):
            missing = []
            if not driver_1:
                missing.append(driver_1_id)
            if not driver_2:
                missing.append(driver_2_id)
            if not driver_3:
                missing.append(driver_3_id)
            raise HTTPException(
                status_code=404, 
                detail=f"Drivers not found with IDs: {missing}"
            )
        
        # Get constructor
        constructor = self.session.exec(
            select(Teams).where(Teams.id == constructor_id)
        ).first()
        
        if not constructor:
            raise HTTPException(status_code=404, detail="Constructor not found")
        
        # Calculate total cost
        driver_costs = []
        for driver in drivers:
            cost = self.pricing_service.calculate_price(driver.id)
            driver_costs.append(cost)
            logger.debug(f"Driver {driver.full_name}: ${cost / 1_000_000:.1f}M")
        
        total_driver_cost = sum(driver_costs)
        logger.debug(f"Total driver cost: ${total_driver_cost / 1_000_000:.1f}M")
        
        # Teams don't have price in current schema, default to 0 for now
        # TODO: Add team pricing when market system is fully implemented
        constructor_cost = 0
        
        total_cost = total_driver_cost + constructor_cost
        budget_remaining = self.INITIAL_BUDGET - total_cost
        
        logger.debug(f"Budget calculation: {self.INITIAL_BUDGET / 1_000_000:.1f}M - {total_cost / 1_000_000:.1f}M = {budget_remaining / 1_000_000:.1f}M")
        
        # Validate budget
        if budget_remaining < 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Budget exceeded. Total cost: ${total_cost / 1_000_000:.1f}M, Budget: ${self.INITIAL_BUDGET / 1_000_000:.1f}M"
            )
        
        return budget_remaining


class TeamValidationService:
    """
    Domain service for validating team rules
    """
    
    @staticmethod
    def validate_unique_drivers(driver_1_id: int, driver_2_id: int, driver_3_id: int) -> None:
        """
        Validate that all drivers are unique
        
        Args:
            driver_1_id: ID of first driver
            driver_2_id: ID of second driver
            driver_3_id: ID of third driver
            
        Raises:
            HTTPException: If drivers are not unique
        """
        driver_ids = [driver_1_id, driver_2_id, driver_3_id]
        if len(set(driver_ids)) != 3:
            raise HTTPException(status_code=400, detail="All drivers must be unique")
    
    @staticmethod
    def validate_driver_in_team(
        driver_id: int, 
        driver_1_id: int, 
        driver_2_id: int, 
        driver_3_id: int, 
        reserve_driver_id: int | None
    ) -> int | None:
        """
        Validate that a driver is in the team and return which slot (1, 2, 3, or None for reserve)
        
        Args:
            driver_id: ID of the driver to check
            driver_1_id: ID of driver in slot 1
            driver_2_id: ID of driver in slot 2
            driver_3_id: ID of driver in slot 3
            reserve_driver_id: ID of reserve driver
            
        Returns:
            int | None: Slot number (1, 2, 3) or None if driver is reserve
            
        Raises:
            HTTPException: If driver is not in the team
        """
        if driver_1_id == driver_id:
            return 1
        elif driver_2_id == driver_id:
            return 2
        elif driver_3_id == driver_id:
            return 3
        elif reserve_driver_id == driver_id:
            raise HTTPException(400, "Driver is already in reserve position")
        else:
            raise HTTPException(400, "Driver not found in team")
