"""Mappers for converting between domain entities and infrastructure models"""
from f1_api.features.market.domain.entities import (
    DriverOwnership,
    MarketTransaction,
    BuyoutHistory,
)
from f1_api.features.market.infrastructure.models import (
    DriverOwnershipModel,
    MarketTransactionModel,
    BuyoutClauseHistoryModel,
)


class OwnershipMapper:
    """Convert between DriverOwnership entity and DriverOwnershipModel"""
    
    @staticmethod
    def to_entity(model: DriverOwnershipModel) -> DriverOwnership:
        """
        Convert SQLModel to domain entity.
        
        Args:
            model: Database model instance
            
        Returns:
            Domain entity with business logic
        """
        return DriverOwnership(
            driver_id=model.driver_id,
            league_id=model.league_id,
            owner_id=model.owner_id,
            is_listed_for_sale=model.is_listed_for_sale,
            acquisition_price=model.acquisition_price,
            asking_price=model.asking_price,
            locked_until=model.locked_until,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
    
    @staticmethod
    def to_model(entity: DriverOwnership) -> DriverOwnershipModel:
        """
        Convert domain entity to SQLModel.
        
        Args:
            entity: Domain entity instance
            
        Returns:
            Database model ready for persistence
        """
        return DriverOwnershipModel(
            driver_id=entity.driver_id,
            league_id=entity.league_id,
            owner_id=entity.owner_id,
            is_listed_for_sale=entity.is_listed_for_sale,
            acquisition_price=entity.acquisition_price,
            asking_price=entity.asking_price,
            locked_until=entity.locked_until,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    @staticmethod
    def update_model(model: DriverOwnershipModel, entity: DriverOwnership) -> None:
        """
        Update existing model with entity data (in-place).
        
        Args:
            model: Existing database model
            entity: Domain entity with updated data
        """
        model.owner_id = entity.owner_id
        model.is_listed_for_sale = entity.is_listed_for_sale
        model.acquisition_price = entity.acquisition_price
        model.asking_price = entity.asking_price
        model.locked_until = entity.locked_until
        model.updated_at = entity.updated_at


class TransactionMapper:
    """Convert between MarketTransaction entity and MarketTransactionModel"""
    
    @staticmethod
    def to_entity(model: MarketTransactionModel) -> MarketTransaction:
        """
        Convert SQLModel to domain entity.
        
        Args:
            model: Database model instance
            
        Returns:
            Domain entity with business logic
        """
        return MarketTransaction(
            id=model.id,
            driver_id=model.driver_id,
            league_id=model.league_id,
            buyer_id=model.buyer_id,
            seller_id=model.seller_id,
            transaction_price=model.transaction_price,
            transaction_type=model.transaction_type,
            transaction_date=model.transaction_date,
        )
    
    @staticmethod
    def to_model(entity: MarketTransaction) -> MarketTransactionModel:
        """
        Convert domain entity to SQLModel.
        
        Args:
            entity: Domain entity instance
            
        Returns:
            Database model ready for persistence
        """
        return MarketTransactionModel(
            id=entity.id,
            driver_id=entity.driver_id,
            league_id=entity.league_id,
            buyer_id=entity.buyer_id,
            seller_id=entity.seller_id,
            transaction_price=entity.transaction_price,
            transaction_type=entity.transaction_type,
            transaction_date=entity.transaction_date,
        )


class BuyoutMapper:
    """Convert between BuyoutHistory entity and BuyoutClauseHistoryModel"""
    
    @staticmethod
    def to_entity(model: BuyoutClauseHistoryModel) -> BuyoutHistory:
        """
        Convert SQLModel to domain entity.
        
        Args:
            model: Database model instance
            
        Returns:
            Domain entity with business logic
        """
        return BuyoutHistory(
            id=model.id,
            league_id=model.league_id,
            buyer_id=model.buyer_id,
            victim_id=model.victim_id,
            driver_id=model.driver_id,
            buyout_price=model.buyout_price,
            buyout_date=model.buyout_date,
            season_year=model.season_year,
        )
    
    @staticmethod
    def to_model(entity: BuyoutHistory) -> BuyoutClauseHistoryModel:
        """
        Convert domain entity to SQLModel.
        
        Args:
            entity: Domain entity instance
            
        Returns:
            Database model ready for persistence
        """
        return BuyoutClauseHistoryModel(
            id=entity.id,
            league_id=entity.league_id,
            buyer_id=entity.buyer_id,
            victim_id=entity.victim_id,
            driver_id=entity.driver_id,
            buyout_price=entity.buyout_price,
            buyout_date=entity.buyout_date,
            season_year=entity.season_year,
        )
