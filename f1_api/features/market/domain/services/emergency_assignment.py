"""Emergency assignment domain service"""
from typing import Tuple, Optional
from datetime import datetime, timedelta
from ..entities import DriverOwnership, MarketTransaction
from ..value_objects import DriverPrice


class EmergencyAssignmentService:
    """
    Domain service for emergency driver assignments.
    
    Handles special cases where admin intervention is needed:
    - Driver retirement/absence
    - Technical issues
    - User account problems
    - Corrective actions
    """
    
    # Emergency assignment constants
    EMERGENCY_LOCK_DAYS = 3  # Shorter lock for emergency assignments
    EMERGENCY_PRICE_DISCOUNT = 0.5  # 50% discount on emergency assignments
    
    @classmethod
    def create_emergency_assignment(
        cls,
        driver_id: int,
        league_id: int,
        user_id: int,
        reason: str,
        _admin_id: int,
        override_price: Optional[float] = None,
    ) -> Tuple[DriverOwnership, MarketTransaction]:
        """
        Create emergency driver assignment.
        
        Args:
            driver_id: Driver to assign
            league_id: League context
            user_id: User receiving driver
            reason: Reason for emergency assignment
            admin_id: Admin authorizing assignment
            override_price: Optional price override (default: discounted rate)
            
        Returns:
            Tuple of (DriverOwnership, MarketTransaction)
        """
        # Calculate emergency price
        if override_price is not None:
            price = override_price
        else:
            # Default to heavily discounted emergency price
            base_price = DriverPrice(5_000_000)  # Default $5M
            discounted = base_price.apply_discount(cls.EMERGENCY_PRICE_DISCOUNT)
            price = discounted.amount
        
        # Create ownership with emergency lock period
        lock_until = datetime.now() + timedelta(days=cls.EMERGENCY_LOCK_DAYS)
        
        ownership = DriverOwnership(
            driver_id=driver_id,
            league_id=league_id,
            owner_id=user_id,
            is_listed_for_sale=False,
            acquisition_price=price,
            asking_price=None,
            locked_until=lock_until,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        # Create transaction record for audit trail
        transaction = MarketTransaction(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=user_id,
            transaction_price=price,
            transaction_type="emergency_assignment",
            seller_id=None,  # No seller in emergency assignments
            transaction_date=datetime.now(),
        )
        
        return ownership, transaction
    
    @classmethod
    def validate_emergency_assignment(
        cls,
        driver_id: int,
        user_id: int,
        admin_id: int,
        reason: str,
    ) -> Tuple[bool, str]:
        """
        Validate emergency assignment request.
        
        Args:
            driver_id: Driver to assign
            user_id: Target user
            admin_id: Admin requesting assignment
            reason: Reason for assignment
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate reason is provided
        if not reason or len(reason.strip()) < 10:
            return False, "Emergency assignment requires detailed reason (min 10 characters)."
        
        # In a real system, would validate:
        # - Admin has appropriate permissions
        # - User account is valid
        # - Driver exists
        # For now, basic validation only
        
        if admin_id <= 0:
            return False, "Invalid admin ID."
        
        if user_id <= 0:
            return False, "Invalid user ID."
        
        if driver_id <= 0:
            return False, "Invalid driver ID."
        
        return True, ""
    
    @classmethod
    def create_corrective_reassignment(
        cls,
        original_ownership: DriverOwnership,
        new_owner_id: int,
        _reason: str,
        _admin_id: int,
    ) -> Tuple[DriverOwnership, MarketTransaction]:
        """
        Create corrective reassignment (fix incorrect ownership).
        
        Args:
            original_ownership: Current ownership to correct
            new_owner_id: Correct owner
            reason: Reason for correction
            admin_id: Admin authorizing correction
            
        Returns:
            Tuple of (corrected DriverOwnership, MarketTransaction)
        """
        # Maintain original acquisition price for corrections
        ownership = DriverOwnership(
            driver_id=original_ownership.driver_id,
            league_id=original_ownership.league_id,
            owner_id=new_owner_id,
            is_listed_for_sale=False,
            acquisition_price=original_ownership.acquisition_price,
            asking_price=None,
            locked_until=None,  # No lock on corrections
            created_at=original_ownership.created_at,
            updated_at=datetime.now(),
        )
        
        # Record transaction for audit
        transaction = MarketTransaction(
            driver_id=original_ownership.driver_id,
            league_id=original_ownership.league_id,
            buyer_id=new_owner_id,
            transaction_price=0,  # No cost for corrections
            transaction_type="emergency_assignment",
            seller_id=original_ownership.owner_id,
            transaction_date=datetime.now(),
        )
        
        return ownership, transaction
    
    @classmethod
    def create_compensation_assignment(
        cls,
        driver_id: int,
        league_id: int,
        user_id: int,
        _reason: str,
        _admin_id: int,
    ) -> Tuple[DriverOwnership, MarketTransaction]:
        """
        Create compensation assignment (free driver for user issues).
        
        Args:
            driver_id: Driver to assign as compensation
            league_id: League context
            user_id: User receiving compensation
            reason: Reason for compensation
            admin_id: Admin authorizing compensation
            
        Returns:
            Tuple of (DriverOwnership, MarketTransaction)
        """
        # Compensation drivers are free and unlocked
        ownership = DriverOwnership(
            driver_id=driver_id,
            league_id=league_id,
            owner_id=user_id,
            is_listed_for_sale=False,
            acquisition_price=0,  # Free compensation
            asking_price=None,
            locked_until=None,  # Not locked
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        transaction = MarketTransaction(
            driver_id=driver_id,
            league_id=league_id,
            buyer_id=user_id,
            transaction_price=0,
            transaction_type="emergency_assignment",
            seller_id=None,
            transaction_date=datetime.now(),
        )
        
        return ownership, transaction
    
    @classmethod
    def log_emergency_action(
        cls,
        action_type: str,
        driver_id: int,
        user_id: int,
        admin_id: int,
        reason: str,
    ) -> dict:
        """
        Create log entry for emergency action.
        
        Args:
            action_type: Type of emergency action
            driver_id: Driver affected
            user_id: User affected
            admin_id: Admin who performed action
            reason: Reason for action
            
        Returns:
            Log entry dictionary
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "action_type": action_type,
            "driver_id": driver_id,
            "user_id": user_id,
            "admin_id": admin_id,
            "reason": reason,
            "status": "completed",
        }
