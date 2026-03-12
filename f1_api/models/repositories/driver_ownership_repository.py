from sqlmodel import Session, select
from f1_api.features.market.infrastructure.models.ownership_model import DriverOwnershipModel

class DriverOwnershipRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_driver_and_league(self, driver_id: int, league_id: int) -> DriverOwnershipModel | None:
        """Obtiene la propiedad de un piloto en una liga específica."""
        return self.session.exec(
            select(DriverOwnershipModel).where(
                DriverOwnershipModel.driver_id == driver_id,
                DriverOwnershipModel.league_id == league_id
            )
        ).first()
    
    def get_all_by_league(self, league_id: int) -> list[DriverOwnershipModel]:
        """Obtiene todas las propiedades de pilotos en una liga."""
        return self.session.exec(
            select(DriverOwnershipModel).where(
                DriverOwnershipModel.league_id == league_id
            )
        ).all()
    
    def get_owned_by_user_in_league(self, user_id: int, league_id: int) -> list[DriverOwnershipModel]:
        """Obtiene todos los pilotos que posee un usuario en una liga."""
        print(f"[OWNERSHIP REPO] Querying for ownerships: owner_id={user_id}, league_id={league_id}")
        results = self.session.exec(
            select(DriverOwnershipModel).where(
                DriverOwnershipModel.owner_id == user_id,
                DriverOwnershipModel.league_id == league_id
            )
        ).all()
        print(f"[OWNERSHIP REPO] Found {len(results)} ownerships for user_id={user_id} in league_id={league_id}")
        if results:
            print(f"[OWNERSHIP REPO] Driver IDs: {[r.driver_id for r in results]}")
        return results
    
    def get_free_drivers_in_league(self, league_id: int) -> list[DriverOwnershipModel]:
        """Obtiene todos los pilotos libres (sin dueño) en una liga."""
        return self.session.exec(
            select(DriverOwnershipModel).where(
                DriverOwnershipModel.league_id == league_id,
                DriverOwnershipModel.owner_id == None
            )
        ).all()
    
    def get_drivers_for_sale_in_league(self, league_id: int) -> list[DriverOwnershipModel]:
        """Obtiene todos los pilotos en venta en una liga."""
        return self.session.exec(
            select(DriverOwnershipModel).where(
                DriverOwnershipModel.league_id == league_id,
                DriverOwnershipModel.is_listed_for_sale == True
            )
        ).all()
    
    def create(self, ownership: DriverOwnershipModel) -> DriverOwnershipModel:
        """Crea un nuevo registro de propiedad."""
        self.session.add(ownership)
        return ownership
    
    def update(self, ownership: DriverOwnershipModel) -> DriverOwnershipModel:
        """Actualiza un registro de propiedad existente."""
        self.session.add(ownership)
        return ownership
    
    def delete(self, ownership: DriverOwnershipModel):
        """Elimina un registro de propiedad."""
        self.session.delete(ownership)
