"""Use case: Execute buyout clause"""
from datetime import datetime
from typing import Tuple

from f1_api.features.market.domain.entities import (
    MarketTransaction,
    BuyoutHistory,
)
from f1_api.features.market.domain.interfaces import (
    IOwnershipRepository,
    ITransactionRepository,
    IBuyoutRepository,
)
from f1_api.features.market.domain.services import BuyoutValidator
from f1_api.features.market.domain.value_objects import LockPeriod
from f1_api.features.market.application.dtos.requests import BuyoutClauseRequest
from f1_api.features.market.application.dtos.responses import (
    PurchaseResultResponse,
    ValidationErrorResponse,
    DriverOwnershipResponse,
    MarketTransactionResponse,
)


class BuyoutClauseUseCase:
    """
    Use case for executing a buyout clause.
    
    Business rules:
    - Buyer can force-purchase from another user at 130% of acquisition price
    - Limited to 2 buyouts per user pair per season
    - Driver must be owned by victim (not free agent)
    - Buyer must have sufficient budget
    - Driver becomes locked after buyout
    - Transaction and buyout history are recorded
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transaction_repo: ITransactionRepository,
        buyout_repo: IBuyoutRepository,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            transaction_repo: Repository for transaction operations
            buyout_repo: Repository for buyout history operations
        """
        self.ownership_repo = ownership_repo
        self.transaction_repo = transaction_repo
        self.buyout_repo = buyout_repo
    
    def execute(
        self,
        request: BuyoutClauseRequest,
        current_budget: float,
    ) -> Tuple[bool, PurchaseResultResponse | ValidationErrorResponse]:
        """
        Execute buyout clause purchase.
        
        Args:
            request: Buyout request with driver, buyer, and victim info
            current_budget: Buyer's current available budget
            
        Returns:
            Tuple of (success, response)
            - success: Whether buyout was successful
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
        
        # Validate ownership
        if not ownership.is_owned_by(request.victim_id):
            return False, ValidationErrorResponse(
                error="Driver is not owned by the specified victim",
                error_code="WRONG_OWNER",
            )
        
        # Validate buyer is not victim
        if request.buyer_id == request.victim_id:
            return False, ValidationErrorResponse(
                error="Cannot buyout from yourself",
                error_code="SELF_BUYOUT",
            )
        
        # Get buyout history count
        buyout_count = self.buyout_repo.count_buyouts_between_users(
            buyer_id=request.buyer_id,
            victim_id=request.victim_id,
            league_id=request.league_id,
            season=request.season_year,
        )
        
        # Validate buyout
        is_valid, error_msg, buyout_price = BuyoutValidator.validate_buyout(
            ownership=ownership,
            buyer_id=request.buyer_id,
            victim_id=request.victim_id,
            buyer_budget=current_budget,
            previous_buyouts_count=buyout_count,
        )
        
        if not is_valid or buyout_price is None:
            return False, ValidationErrorResponse(
                error=error_msg,
                error_code="INVALID_BUYOUT",
            )
        
        # Calculate lock period
        lock_period = LockPeriod.default()
        unlock_date = lock_period.calculate_unlock_date()
        
        # Update ownership
        ownership.owner_id = request.buyer_id
        ownership.acquisition_price = buyout_price
        ownership.locked_until = unlock_date
        ownership.is_listed_for_sale = False
        ownership.asking_price = None
        ownership.updated_at = datetime.now()
        
        # Save ownership
        updated_ownership = self.ownership_repo.update(ownership)
        
        # Create transaction record
        transaction = MarketTransaction(
            driver_id=request.driver_id,
            league_id=request.league_id,
            buyer_id=request.buyer_id,
            seller_id=request.victim_id,
            transaction_price=buyout_price,
            transaction_type="buyout_clause",
            transaction_date=datetime.now(),
        )
        
        created_transaction = self.transaction_repo.create(transaction)
        
        # Create buyout history record
        buyout_history = BuyoutHistory(
            league_id=request.league_id,
            buyer_id=request.buyer_id,
            victim_id=request.victim_id,
            driver_id=request.driver_id,
            buyout_price=buyout_price,
            season_year=request.season_year,
            buyout_date=datetime.now(),
        )
        
        self.buyout_repo.create(buyout_history)
        
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
        
        new_budget = current_budget - buyout_price
        
        # Build success response
        return True, PurchaseResultResponse(
            success=True,
            message=f"Successfully bought out driver for ${buyout_price / 1_000_000:.1f}M",
            ownership=ownership_response,
            transaction=transaction_response,
            budget_remaining=new_budget,
            budget_remaining_formatted=f"${new_budget / 1_000_000:.1f}M",
        )
