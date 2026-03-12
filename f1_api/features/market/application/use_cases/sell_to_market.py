"""Use case: Sell driver to market (release to free agency)"""
from datetime import datetime
from typing import Tuple

from f1_api.features.market.domain.entities import MarketTransaction
from f1_api.features.market.domain.interfaces import (
    IOwnershipRepository,
    ITransactionRepository,
)
from f1_api.features.market.application.dtos.requests import SellToMarketRequest
from f1_api.features.market.application.dtos.responses import (
    MarketTransactionResponse,
    ValidationErrorResponse,
)
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl

# Constants
SELL_TO_MARKET_REFUND = 0.8  # 80% refund when quick selling


class SellToMarketUseCase:
    """
    Use case for selling a driver to the market (releasing to free agency).
    
    Business rules:
    - Driver must be owned by the user
    - Driver must not be locked
    - Driver becomes a free agent (owner_id = None)
    - Transaction is recorded for audit
    - No payment received (driver released voluntarily)
    """
    
    def __init__(
        self,
        ownership_repo: IOwnershipRepository,
        transaction_repo: ITransactionRepository,
        user_teams_repo: UserTeamsRepositoryImpl,
    ):
        """
        Initialize use case with required repositories.
        
        Args:
            ownership_repo: Repository for driver ownership operations
            transaction_repo: Repository for transaction operations
            user_teams_repo: Repository for user team operations
        """
        self.ownership_repo = ownership_repo
        self.transaction_repo = transaction_repo
        self.user_teams_repo = user_teams_repo
    
    def execute(
        self, request: SellToMarketRequest
    ) -> Tuple[bool, MarketTransactionResponse | ValidationErrorResponse]:
        """
        Execute driver sale to market (release to free agency).
        
        Args:
            request: Sale request with driver and owner info
            
        Returns:
            Tuple of (success, response)
            - success: Whether sale was successful
            - response: MarketTransactionResponse on success, ValidationErrorResponse on failure
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
        
        # Validate can be sold
        can_sell, reason = ownership.can_be_sold()
        if not can_sell:
            return False, ValidationErrorResponse(
                error=reason,
                error_code="CANNOT_SELL",
            )
        
        # Check minimum driver count (must keep at least 3 for lineup)
        current_driver_count = len(
            self.ownership_repo.get_owned_by_user_in_league(
                request.user_id, request.league_id
            )
        )
        if current_driver_count <= 3:
            return False, ValidationErrorResponse(
                error="Cannot sell driver. You must maintain at least 3 drivers for your lineup.",
                error_code="MINIMUM_DRIVERS",
            )
        
        # Get seller's team
        seller_team = self.user_teams_repo.get_by_league_and_user(
            request.league_id, request.user_id
        )
        if seller_team is None:
            return False, ValidationErrorResponse(
                error="Team not found",
                error_code="TEAM_NOT_FOUND",
            )
        
        # Check if we're selling from main lineup (driver_1, driver_2, or driver_3)
        # If so, we MUST have a reserve driver to shift into the empty slot
        # because driver_3_id has a NOT NULL constraint in the database
        is_selling_from_main_lineup = (
            seller_team.driver_1_id == request.driver_id or
            seller_team.driver_2_id == request.driver_id or
            seller_team.driver_3_id == request.driver_id
        )
        
        if is_selling_from_main_lineup and seller_team.reserve_driver_id is None:
            return False, ValidationErrorResponse(
                error="Cannot sell driver from main lineup without a reserve driver. You must have 4 drivers total.",
                error_code="NO_RESERVE_DRIVER",
            )
        
        # Calculate refund (80% of acquisition price)
        refund = int(ownership.acquisition_price * SELL_TO_MARKET_REFUND)
        
        # Release to market (make free agent)
        ownership.release_to_market()
        ownership.updated_at = datetime.now()
        
        # Save ownership
        self.ownership_repo.update(ownership)
        
        # Remove driver from team and reorganize slots
        if seller_team.driver_1_id == request.driver_id:
            seller_team.driver_1_id = seller_team.driver_2_id
            seller_team.driver_2_id = seller_team.driver_3_id
            seller_team.driver_3_id = seller_team.reserve_driver_id  # type: ignore
            seller_team.reserve_driver_id = None
        elif seller_team.driver_2_id == request.driver_id:
            seller_team.driver_2_id = seller_team.driver_3_id
            seller_team.driver_3_id = seller_team.reserve_driver_id  # type: ignore
            seller_team.reserve_driver_id = None
        elif seller_team.driver_3_id == request.driver_id:
            seller_team.driver_3_id = seller_team.reserve_driver_id  # type: ignore
            seller_team.reserve_driver_id = None
        elif seller_team.reserve_driver_id == request.driver_id:
            seller_team.reserve_driver_id = None
        
        # Update budget with refund
        seller_team.budget_remaining = int(seller_team.budget_remaining + refund)
        seller_team.updated_at = datetime.now()
        # Team changes will be saved via repository context
        
        # Create transaction record
        transaction = MarketTransaction(
            driver_id=request.driver_id,
            league_id=request.league_id,
            buyer_id=request.user_id,  # Same user (receiving refund)
            seller_id=request.user_id,
            transaction_price=refund,  # Refund amount
            transaction_type="sell_to_market",
            transaction_date=datetime.now(),
        )
        
        created_transaction = self.transaction_repo.create(transaction)
        
        # Build success response
        return True, MarketTransactionResponse(
            id=created_transaction.id,
            driver_id=created_transaction.driver_id,
            league_id=created_transaction.league_id,
            buyer_id=created_transaction.buyer_id,
            seller_id=created_transaction.seller_id,
            transaction_price=created_transaction.transaction_price,
            transaction_type=created_transaction.transaction_type,
            transaction_date=created_transaction.transaction_date,
        )
