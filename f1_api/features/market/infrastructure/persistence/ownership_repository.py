"""Driver ownership repository implementation"""
from typing import Optional
from sqlmodel import Session, select

from f1_api.features.market.domain.entities import DriverOwnership
from f1_api.features.market.infrastructure.models import DriverOwnershipModel
from f1_api.features.market.infrastructure.mappers import OwnershipMapper


class OwnershipRepository:
    """
    SQLAlchemy implementation of IOwnershipRepository.
    
    Handles persistence operations for driver ownership, mapping between
    domain entities and database models.
    """
    
    def __init__(self, session: Session):
        """
        Initialize repository with database session.
        
        Args:
            session: SQLAlchemy session for database operations
        """
        self.session = session
    
    def get_by_driver_and_league(
        self, 
        driver_id: int, 
        league_id: int
    ) -> Optional[DriverOwnership]:
        """
        Get ownership record for a specific driver in a league.
        
        Args:
            driver_id: Driver identifier
            league_id: League identifier
            
        Returns:
            DriverOwnership if found, None otherwise
        """
        statement = select(DriverOwnershipModel).where(
            DriverOwnershipModel.driver_id == driver_id,
            DriverOwnershipModel.league_id == league_id
        )
        model = self.session.exec(statement).first()
        
        if model is None:
            return None
        
        return OwnershipMapper.to_entity(model)
    
    def get_free_drivers_in_league(self, league_id: int) -> list[DriverOwnership]:
        """
        Get all drivers without owners in a league (free agents).
        
        Args:
            league_id: League identifier
            
        Returns:
            List of driver ownerships where owner_id is None
        """
        statement = select(DriverOwnershipModel).where(
            DriverOwnershipModel.league_id == league_id,
            DriverOwnershipModel.owner_id == None
        )
        models = self.session.exec(statement).all()
        
        return [OwnershipMapper.to_entity(model) for model in models]
    
    def get_drivers_for_sale_in_league(
        self, 
        league_id: int
    ) -> list[DriverOwnership]:
        """
        Get all drivers listed for sale in a league.
        
        Args:
            league_id: League identifier
            
        Returns:
            List of driver ownerships where is_listed_for_sale is True
        """
        statement = select(DriverOwnershipModel).where(
            DriverOwnershipModel.league_id == league_id,
            DriverOwnershipModel.is_listed_for_sale == True  # noqa: E712
        )
        models = self.session.exec(statement).all()
        
        return [OwnershipMapper.to_entity(model) for model in models]
    
    def get_owned_by_user_in_league(
        self, 
        user_id: int, 
        league_id: int
    ) -> list[DriverOwnership]:
        """
        Get all drivers owned by a specific user in a league.
        
        Args:
            user_id: User identifier
            league_id: League identifier
            
        Returns:
            List of driver ownerships belonging to the user
        """
        statement = select(DriverOwnershipModel).where(
            DriverOwnershipModel.league_id == league_id,
            DriverOwnershipModel.owner_id == user_id
        )
        models = self.session.exec(statement).all()
        
        return [OwnershipMapper.to_entity(model) for model in models]
    
    def update(self, ownership: DriverOwnership) -> DriverOwnership:
        """
        Update an existing driver ownership record.
        
        Args:
            ownership: DriverOwnership entity to update
            
        Returns:
            Updated DriverOwnership entity
        """
        # Fetch existing model
        statement = select(DriverOwnershipModel).where(
            DriverOwnershipModel.driver_id == ownership.driver_id,
            DriverOwnershipModel.league_id == ownership.league_id
        )
        model = self.session.exec(statement).first()
        
        if model is None:
            # If doesn't exist, create new
            model = OwnershipMapper.to_model(ownership)
            self.session.add(model)
        else:
            # Update existing
            OwnershipMapper.update_model(model, ownership)
        
        self.session.commit()
        self.session.refresh(model)
        
        return OwnershipMapper.to_entity(model)

    def create(self, ownership: DriverOwnership) -> DriverOwnership:
        """
        Create a new driver ownership record.

        Args:
            ownership: DriverOwnership entity to persist

        Returns:
            Created DriverOwnership entity
        """
        model = OwnershipMapper.to_model(ownership)
        self.session.add(model)
        self.session.flush()
        return OwnershipMapper.to_entity(model)
