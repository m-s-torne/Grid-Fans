"""Market repositories"""
from sqlmodel import Session, select, desc
from f1_api.features.market.infrastructure.models import MarketTransactionModel as MarketTransactions

class MarketTransactionsRepository:
    """Repository CRUD for market transactions"""
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, transaction_id: int) -> MarketTransactions | None:
        """Obtiene una transacción por su ID."""
        return self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.id == transaction_id
            )
        ).first()
    
    def get_all_by_league(self, league_id: int) -> list[MarketTransactions]:
        """Obtiene todas las transacciones de una liga."""
        return list(self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.league_id == league_id
            ).order_by(desc(MarketTransactions.transaction_date))
        ).all())
    
    def get_by_user_in_league(self, user_id: int, league_id: int) -> list[MarketTransactions]:
        """Obtiene todas las transacciones de un usuario en una liga (como comprador o vendedor)."""
        return list(self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.league_id == league_id,
                (MarketTransactions.buyer_id == user_id) | (MarketTransactions.seller_id == user_id)
            ).order_by(desc(MarketTransactions.transaction_date))
        ).all())
    
    def get_by_driver_in_league(self, driver_id: int, league_id: int) -> list[MarketTransactions]:
        """Obtiene todas las transacciones de un piloto específico en una liga."""
        return list(self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.driver_id == driver_id,
                MarketTransactions.league_id == league_id
            ).order_by(desc(MarketTransactions.transaction_date))
        ).all())
    
    def get_recent_transactions(self, league_id: int, limit: int = 10) -> list[MarketTransactions]:
        """Obtiene las últimas N transacciones de una liga."""
        return list(self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.league_id == league_id
            ).order_by(desc(MarketTransactions.transaction_date)).limit(limit)
        ).all())
    
    def create(self, transaction: MarketTransactions) -> MarketTransactions:
        """Crea una nueva transacción."""
        self.session.add(transaction)
        return transaction
    
    def get_purchase_count_for_driver(self, driver_id: int, league_id: int) -> int:
        """Cuenta cuántas veces ha sido comprado un piloto en una liga."""
        transactions = self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.driver_id == driver_id,
                MarketTransactions.league_id == league_id,
                (MarketTransactions.transaction_type == 'buy_from_market') | 
                (MarketTransactions.transaction_type == 'buy_from_user')
            )
        ).all()
        return len(transactions)
    
    def get_sale_count_for_driver(self, driver_id: int, league_id: int) -> int:
        """Cuenta cuántas veces ha sido vendido un piloto en una liga."""
        transactions = self.session.exec(
            select(MarketTransactions).where(
                MarketTransactions.driver_id == driver_id,
                MarketTransactions.league_id == league_id,
                MarketTransactions.transaction_type == 'sell_to_market'
            )
        ).all()
        return len(transactions)
