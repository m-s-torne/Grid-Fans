"""Use case: List driver for sale"""
from datetime import datetime
from typing import Tuple


from f1_api.features.market.domain.interfaces import IOwnershipRepository
from f1_api.features.market.domain.value_objects import DriverPrice
from f1_api.features.market.application.dtos.requests import ListDriverForSaleRequest
from f1_api.features.market.application.dtos.responses import (
    DriverOwnershipResponse,
    ValidationErrorResponse,
)


class ListDriverForSaleUseCase:
    """
    Use case for listing a driver for sale.
    
    Business rules:
    - Driver must be owned by the user
    - Driver must not be locked
    - Driver must not already be listed
    - Asking price must be valid (min/max constraints)
    """
    
    def __init__(self, ownership_repo: IOwnershipRepository):
        """
        Initialize use case with required repository.
        
        Args:
            ownership_repo: Repository for driver ownership operations
        """
        self.ownership_repo = ownership_repo
    
    def execute(
        self, request: ListDriverForSaleRequest
    ) -> Tuple[bool, DriverOwnershipResponse | ValidationErrorResponse]:
        """
        Execute driver listing for sale.
        
        Args:
            request: Listing request with driver, owner, and asking price
            
        Returns:
            Tuple of (success, response)
            - success: Whether listing was successful
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
        
        # Validate can list (not locked, not already listed)
        can_list, reason = ownership.can_be_listed()
        if not can_list:
            return False, ValidationErrorResponse(
                error=reason,
                error_code="CANNOT_LIST",
            )
        
        # Validate asking price
        if request.asking_price is not None:
            try:
                DriverPrice(request.asking_price)
            except ValueError as e:
                return False, ValidationErrorResponse(
                    error=str(e),
                    error_code="INVALID_PRICE",
                )
        
        # List driver for sale
        ownership.list_for_sale(request.asking_price)
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
            is_locked=False,
        )
