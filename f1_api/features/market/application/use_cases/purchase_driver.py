"""Use case: Purchase driver from market"""
from datetime import datetime
from typing import Tuple

from f1_api.features.market.domain.entities import MarketTransaction
from f1_api.features.market.domain.interfaces import (
    IOwnershipRepository,
    ITransactionRepository,
)
from f1_api.features.market.domain.services import BudgetValidator
from f1_api.features.market.domain.value_objects import LockPeriod
from f1_api.features.market.application.dtos.requests import PurchaseDriverRequest
from f1_api.features.market.application.dtos.responses import (
    PurchaseResultResponse,
    ValidationErrorResponse,
    DriverOwnershipResponse,
    MarketTransactionResponse,
)
from f1_api.features.user_teams.domain.interfaces import UserTeamsRepository


class PurchaseDriverUseCase:
    """
    Use case for purchasing a driver from the free market.
    
    Business rules:
    - Driver must be a free agent (owner_id = None)
    - Buyer must have sufficient budget
    - Driver becomes locked after purchase
    - Transaction is recorded for audit
    - Purchase price is the driver's current acquisition_price
    - Driver is added to buyer's team
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transaction_repo: ITransactionRepository,
        user_teams_repo: UserTeamsRepository,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            transaction_repo: Repository for transaction operations
            user_teams_repo: Repository for user teams operations
        """
        self.ownership_repo = ownership_repo
        self.transaction_repo = transaction_repo
        self.user_teams_repo = user_teams_repo
    
    def execute(
        self,
        request: PurchaseDriverRequest,
        current_budget: float,
    ) -> Tuple[bool, PurchaseResultResponse | ValidationErrorResponse]:
        """
        Execute driver purchase from market.
        
        Args:
            request: Purchase request with driver, buyer info
            current_budget: Buyer's current available budget
            
        Returns:
            Tuple of (success, response)
            - success: Whether purchase was successful
            - response: PurchaseResultResponse on success, ValidationErrorResponse on failure
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
        
        # Validate driver is free agent
        if not ownership.is_free_agent():
            return False, ValidationErrorResponse(
                error="Driver is not a free agent",
                error_code="NOT_FREE_AGENT",
            )
        
        # Purchase price is the current acquisition_price
        purchase_price = ownership.acquisition_price
        
        # Validate budget
        is_valid, error_msg = BudgetValidator.validate_purchase(
            current_budget=current_budget,
            purchase_price=purchase_price,
        )
        
        if not is_valid:
            return False, ValidationErrorResponse(
                error=error_msg,
                error_code="INSUFFICIENT_BUDGET",
            )
        
        # Calculate lock period
        lock_period = LockPeriod.default()
        unlock_date = lock_period.calculate_unlock_date()
        
        # Update ownership
        ownership.owner_id = request.user_id
        ownership.locked_until = unlock_date
        ownership.is_listed_for_sale = False
        ownership.asking_price = None
        ownership.updated_at = datetime.now()
        
        # Save ownership
        updated_ownership = self.ownership_repo.update(ownership)
        
        # Update team lineup - add driver to buyer's first available slot
        buyer_team = self.user_teams_repo.get_by_league_and_user(
            request.league_id, request.user_id
        )
        
        if buyer_team is None:
            return False, ValidationErrorResponse(
                error="Team not found for buyer",
                error_code="TEAM_NOT_FOUND",
            )
        
        # Add driver to first available slot
        if buyer_team.driver_1_id is None:
            buyer_team.driver_1_id = request.driver_id
        elif buyer_team.driver_2_id is None:
            buyer_team.driver_2_id = request.driver_id
        elif buyer_team.driver_3_id is None:
            buyer_team.driver_3_id = request.driver_id
        elif buyer_team.reserve_driver_id is None:
            buyer_team.reserve_driver_id = request.driver_id
        else:
            return False, ValidationErrorResponse(
                error="All driver slots are full",
                error_code="SLOTS_FULL",
            )
        
        # Update budget
        buyer_team.budget_remaining -= int(purchase_price)
        buyer_team.updated_at = datetime.now()
        
        # Save team changes (commit happens in route handler)
        self.user_teams_repo.session.add(buyer_team)
        
        # Create transaction record
        transaction = MarketTransaction(
            driver_id=request.driver_id,
            league_id=request.league_id,
            buyer_id=request.user_id,
            seller_id=None,  # None = free market
            transaction_price=purchase_price,
            transaction_type="buy_from_market",
            transaction_date=datetime.now(),
        )
        
        created_transaction = self.transaction_repo.create(transaction)
        
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
            is_locked=True,
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
        
        new_budget = current_budget - purchase_price
        
        # Build success response
        return True, PurchaseResultResponse(
            success=True,
            message=f"Successfully purchased driver for ${purchase_price / 1_000_000:.1f}M",
            ownership=ownership_response,
            transaction=transaction_response,
            budget_remaining=new_budget,
            budget_remaining_formatted=f"${new_budget / 1_000_000:.1f}M",
        )
