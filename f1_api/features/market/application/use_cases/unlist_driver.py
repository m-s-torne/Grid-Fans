"""Use case: Unlist driver from sale"""
from datetime import datetime
from typing import Tuple


from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.market.application.dtos.requests import UnlistDriverRequest
from f1_api.features.market.application.dtos.responses import (
    DriverOwnershipResponse,
    ValidationErrorResponse,
)


class UnlistDriverUseCase:
    """
    Use case for unlisting a driver from sale.
    
    Business rules:
    - Driver must be owned by the user
    - Driver must be currently listed for sale
    """
    
    def __init__(self, ownership_repo: IOwnershipRepository):
        """
        Initialize use case with required repository.
        
        Args:
            ownership_repo: Repository for driver ownership operations
        """
        self.ownership_repo = ownership_repo
    
    def execute(
        self, request: UnlistDriverRequest
    ) -> Tuple[bool, DriverOwnershipResponse | ValidationErrorResponse]:
        """
        Execute driver unlisting from sale.
        
        Args:
            request: Unlisting request with driver and owner info
            
        Returns:
            Tuple of (success, response)
            - success: Whether unlisting was successful
            - response: DriverOwnershipResponse on success, ValidationErrorResponse on failure
        """
        # Get existing ownership
        ownership = self.ownership_repo.get_by_driver_and_league(
            request.driver_id, request.league_id
        )
        
        if ownership is None:
            return False, ValidationErrorResponse(
                error="Driver not found in league",
                error_code="DRIVER_NOT_FOUND",
            )
        
        # Validate ownership
        if not ownership.is_owned_by(request.user_id):
            return False, ValidationErrorResponse(
                error="You do not own this driver",
                error_code="NOT_OWNER",
            )
        
        # Validate is listed
        if not ownership.is_listed_for_sale:
            return False, ValidationErrorResponse(
                error="Driver is not currently listed for sale",
                error_code="NOT_LISTED",
            )
        
        # Unlist driver
        ownership.is_listed_for_sale = False
        ownership.asking_price = None
        ownership.updated_at = datetime.now()
        
        # Save ownership
        updated_ownership = self.ownership_repo.update(ownership)
        
        # Build success response
        return True, DriverOwnershipResponse(
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
