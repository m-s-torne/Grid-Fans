"""Market transaction repository implementation"""
from sqlmodel import Session, select, desc

from f1_api.features.market.domain.entities import MarketTransaction
from f1_api.features.market.infrastructure.models import MarketTransactionModel
from f1_api.features.market.infrastructure.mappers import TransactionMapper


class TransactionRepository:
    """
    SQLAlchemy implementation of ITransactionRepository.
    
    Handles persistence operations for market transactions, mapping between
    domain entities and database models.
    """
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session
    
    def create(self, transaction: MarketTransaction) -> MarketTransaction:
        """
        Create a new market transaction record.
        
        Args:
            transaction: MarketTransaction entity to persist
            
        Returns:
            Created MarketTransaction with ID assigned
        """
        model = TransactionMapper.to_model(transaction)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        
        return TransactionMapper.to_entity(model)
    
    def get_by_league(self, league_id: int) -> list[MarketTransaction]:
        """
        Get all market transactions for a specific league.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of all transactions in the league, ordered by date descending
        """
        statement = (
            select(MarketTransactionModel)
            .where(MarketTransactionModel.league_id == league_id)
            .order_by(desc(MarketTransactionModel.transaction_date))
        )
        models = self.session.exec(statement).all()
        
        return [TransactionMapper.to_entity(model) for model in models]
