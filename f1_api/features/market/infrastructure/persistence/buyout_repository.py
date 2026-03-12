"""Buyout clause history repository implementation"""
from sqlmodel import Session, select

from f1_api.features.market.domain.entities import BuyoutHistory
from f1_api.features.market.infrastructure.models import BuyoutClauseHistoryModel
from f1_api.features.market.infrastructure.mappers import BuyoutMapper


class BuyoutRepository:
    """
    SQLAlchemy implementation of IBuyoutRepository.
    
    Handles persistence operations for buyout clause history, mapping between
    domain entities and database models.
    """
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session
    
    def create(self, buyout: BuyoutHistory) -> BuyoutHistory:
        """
        Create a new buyout clause history record.
        
        Args:
            buyout: BuyoutHistory entity to persist
            
        Returns:
            Created BuyoutHistory with ID assigned
        """
        model = BuyoutMapper.to_model(buyout)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        
        return BuyoutMapper.to_entity(model)
    
    def count_buyouts_between_users(
        self, 
        buyer_id: int, 
        victim_id: int, 
        league_id: int,
        season: int
    ) -> int:
        """
        Count how many times buyer has used buyout clause against victim.
        
        This is used to enforce business rules around buyout frequency limits.
        
        Args:
            buyer_id: User who initiated the buyouts
            victim_id: User whose driver was bought out
            league_id: League identifier
            season: Season year
            
        Returns:
            Count of buyout transactions matching the criteria
        """
        statement = select(BuyoutClauseHistoryModel).where(
            BuyoutClauseHistoryModel.buyer_id == buyer_id,
            BuyoutClauseHistoryModel.victim_id == victim_id,
            BuyoutClauseHistoryModel.league_id == league_id,
            BuyoutClauseHistoryModel.season_year == season
        )
        results = self.session.exec(statement).all()
        
        return len(results)
