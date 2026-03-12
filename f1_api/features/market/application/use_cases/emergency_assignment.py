"""Use case: Emergency driver assignment (admin only)"""
from typing import Tuple

from f1_api.features.market.domain.interfaces import (
    IOwnershipRepository,
    ITransactionRepository,
)
from f1_api.features.market.domain.services import EmergencyAssignmentService
from f1_api.features.market.application.dtos.requests import EmergencyAssignmentRequest
from f1_api.features.market.application.dtos.responses import (
    PurchaseResultResponse,
    ValidationErrorResponse,
    DriverOwnershipResponse,
    MarketTransactionResponse,
)


class EmergencyAssignmentUseCase:
    """
    Use case for emergency driver assignment by admin.
    
    Business rules:
    - Only admins can execute emergency assignments
    - Used for special cases (driver retirement, corrections, compensation)
    - May have reduced lock time and discounted price
    - Requires detailed reason for audit trail
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transaction_repo: ITransactionRepository,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            transaction_repo: Repository for transaction operations
        """
        self.ownership_repo = ownership_repo
        self.transaction_repo = transaction_repo
    
    def execute(
        self, request: EmergencyAssignmentRequest, is_admin: bool = False
    ) -> Tuple[bool, PurchaseResultResponse | ValidationErrorResponse]:
        """
        Execute emergency driver assignment.
        
        Args:
            request: Emergency assignment request
            is_admin: Whether the requester has admin privileges
            
        Returns:
            Tuple of (success, response)
            - success: Whether assignment was successful
            - response: PurchaseResultResponse on success, ValidationErrorResponse on failure
        """
        # Validate admin privileges
        if not is_admin:
            return False, ValidationErrorResponse(
                error="Only admins can execute emergency assignments",
                error_code="UNAUTHORIZED",
            )
        
        # Validate assignment request
        is_valid, error_msg = EmergencyAssignmentService.validate_emergency_assignment(
            driver_id=request.driver_id,
            user_id=request.user_id,
            admin_id=request.admin_id,
            reason=request.reason,
        )
        
        if not is_valid:
            return False, ValidationErrorResponse(
                error=error_msg,
                error_code="INVALID_ASSIGNMENT",
            )
        
        # Create emergency assignment
        ownership, transaction = EmergencyAssignmentService.create_emergency_assignment(
            driver_id=request.driver_id,
            league_id=request.league_id,
            user_id=request.user_id,
            reason=request.reason,
            _admin_id=request.admin_id,
            override_price=request.override_price,
        )
        
        # Save ownership
        updated_ownership = self.ownership_repo.update(ownership)
        
        # Save transaction
        created_transaction = self.transaction_repo.create(transaction)
        
        # Log emergency action (in real system, would log to audit table)
        EmergencyAssignmentService.log_emergency_action(
            action_type="emergency_assignment",
            driver_id=request.driver_id,
            user_id=request.user_id,
            admin_id=request.admin_id,
            reason=request.reason,
        )
        
        # Build response DTOs
        ownership_response = DriverOwnershipResponse(
            driver_id=updated_ownership.driver_id,
            league_id=updated_ownership.league_id,
            owner_id=updated_ownership.owner_id,
            is_listed_for_sale=updated_ownership.is_listed_for_sale,
            acquisition_price=updated_ownership.acquisition_price,
            asking_price=updated_ownership.asking_price,
            locked_until=updated_ownership.locked_until,
            created_at=updated_ownership.created_at,
            updated_at=updated_ownership.updated_at,
            is_free_agent=False,
            is_locked=updated_ownership.is_locked(),
        )
        
        transaction_response = MarketTransactionResponse(
            id=created_transaction.id,
            driver_id=created_transaction.driver_id,
            league_id=created_transaction.league_id,
            seller_id=created_transaction.seller_id,
            buyer_id=created_transaction.buyer_id,
            transaction_price=created_transaction.transaction_price,
            transaction_type=created_transaction.transaction_type,
            transaction_date=created_transaction.transaction_date,
        )
        
        # Build success response
        return True, PurchaseResultResponse(
            success=True,
            message=f"Emergency assignment completed for ${created_transaction.transaction_price / 1_000_000:.1f}M",
            ownership=ownership_response,
            transaction=transaction_response,
            budget_remaining=0,  # Not applicable for emergency assignments
            budget_remaining_formatted="N/A",
        )
