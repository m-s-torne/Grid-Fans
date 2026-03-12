"""Market repository interfaces - Contracts for data access"""
from .i_ownership_repository import IOwnershipRepository
from .i_transaction_repository import ITransactionRepository
from .i_buyout_repository import IBuyoutRepository

__all__ = ["IOwnershipRepository", "ITransactionRepository", "IBuyoutRepository"]
