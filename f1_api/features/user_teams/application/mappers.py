"""
User Teams Application Layer - Mappers
Data transformation utilities for converting between domain models and DTOs
"""
from sqlmodel import Session, select
from f1_api.features.user_teams.domain.models import UserTeams
from f1_api.features.leagues.domain.models import Leagues
from f1_api.features.drivers.domain.models import Drivers
from f1_api.features.teams.domain.models import Teams
from .dtos import UserTeamResponseDTO


class UserTeamMapper:
    """Mapper for converting UserTeams entity to response DTOs"""
    
    @staticmethod
    def to_response_dto(team: UserTeams) -> UserTeamResponseDTO:
        """
        Convert a UserTeams domain model to a UserTeamResponseDTO
        
        Args:
            team: UserTeams domain model
            
        Returns:
            UserTeamResponseDTO: DTO for API response
        """
        return UserTeamResponseDTO(
            id=team.id,
            user_id=team.user_id,
            league_id=team.league_id,
            team_name=team.team_name,
            driver_1_id=team.driver_1_id,
            driver_2_id=team.driver_2_id,
            driver_3_id=team.driver_3_id,
            reserve_driver_id=team.reserve_driver_id,
            constructor_id=team.constructor_id,
            total_points=team.total_points,
            budget_remaining=team.budget_remaining,
            is_active=team.is_active,
            created_at=team.created_at,
            updated_at=team.updated_at
        )


class TeamEnrichmentService:
    """Service for enriching team data with related entities (drivers, leagues, constructors)"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def enrich_team_data(self, team: UserTeams) -> dict:
        """
        Enrich a team with full driver, league, and constructor details
        
        Args:
            team: UserTeams domain model
            
        Returns:
            dict: Enriched team data with full details
        """
        # Get league name
        league = self.session.exec(
            select(Leagues).where(Leagues.id == team.league_id)
        ).first()
        
        # Get drivers info
        driver1 = self.session.exec(
            select(Drivers).where(Drivers.id == team.driver_1_id)
        ).first()
        driver2 = self.session.exec(
            select(Drivers).where(Drivers.id == team.driver_2_id)
        ).first()
        driver3 = self.session.exec(
            select(Drivers).where(Drivers.id == team.driver_3_id)
        ).first()
        
        # Get constructor info
        constructor = self.session.exec(
            select(Teams).where(Teams.id == team.constructor_id)
        ).first()
        
        return {
            "id": team.id,
            "team_name": team.team_name,
            "league_id": team.league_id,
            "league_name": league.name if league else "Unknown League",
            "total_points": team.total_points,
            "budget_remaining": team.budget_remaining,
            "created_at": team.created_at,
            "updated_at": team.updated_at,
            "drivers": self._format_drivers([driver1, driver2, driver3]),
            "constructor": self._format_constructor(constructor)
        }
    
    def _format_drivers(self, drivers: list[Drivers | None]) -> list[dict]:
        """
        Format driver data for response
        
        Args:
            drivers: List of driver entities (can include None)
            
        Returns:
            list[dict]: Formatted driver data
        """
        return [
            {
                "id": driver.id if driver else None,
                "name": driver.full_name if driver else "Unknown Driver",
                "headshot": driver.headshot_url if driver else None
            }
            for driver in drivers
        ]
    
    def _format_constructor(self, constructor: Teams | None) -> dict:
        """
        Format constructor data for response
        
        Args:
            constructor: Teams entity (can be None)
            
        Returns:
            dict: Formatted constructor data
        """
        return {
            "id": constructor.id if constructor else None,
            "name": constructor.team_name if constructor else "Unknown Constructor",
            "logo": f"/teams/{constructor.team_name.lower().replace(' ', '')}.svg" if constructor else None
        }
