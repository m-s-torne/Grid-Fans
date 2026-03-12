"""
User Teams Application Layer - Business Logic Services
Orchestrates domain models and repositories to implement use cases
"""
import logging
from sqlmodel import Session
from fastapi import HTTPException

from ..domain.interfaces import UserTeamsRepository
from ..domain.services import DriverPricingService, BudgetCalculationService, TeamValidationService
from ..domain.exceptions import (
    DuplicateDriverError,
    DriverNotInTeamError,
    DriverAlreadyReserveError,
    DriverNotFoundError,
    ConstructorNotFoundError,
    BudgetExceededError,
)
from .dtos import UserTeamCreateDTO, UserTeamUpdateDTO, UserTeamResponseDTO
from .mappers import UserTeamMapper, TeamEnrichmentService

from f1_api.features.user.domain.interfaces import UserRepository
from f1_api.features.leagues.domain.models import UserLeagueLink
from f1_api.features.leagues.domain.interfaces import UserLeagueLinkRepository
from sqlmodel import select
from datetime import datetime
from f1_api.features.user_teams.domain.models import UserTeams

logger = logging.getLogger(__name__)


class CreateOrUpdateTeamService:
    """
    Service for creating or updating user teams in a league
    Business logic:
    - Validates user exists and is league member
    - Validates driver uniqueness
    - Calculates budget based on driver/constructor prices
    - Creates new team or updates existing
    """
    
    def __init__(
        self,
        session: Session,
        user_teams_repo: UserTeamsRepository,
        user_repo: UserRepository,
        league_link_repo: UserLeagueLinkRepository
    ):
        self.session = session
        self.user_teams_repo = user_teams_repo
        self.user_repo = user_repo
        self.league_link_repo = league_link_repo
        
        # Initialize domain services
        self.pricing_service = DriverPricingService(session)
        self.budget_service = BudgetCalculationService(session, self.pricing_service)
        self.validation_service = TeamValidationService()
    
    def execute(
        self,
        league_id: int,
        team_data: UserTeamUpdateDTO,
        user_id: str
    ) -> UserTeamResponseDTO:
        """
        Create or update a user's team in a specific league
        
        Args:
            league_id: ID of the league for the team
            team_data: UserTeamUpdateDTO object with team data
            user_id: Supabase user ID of the team owner
            
        Returns:
            UserTeamResponseDTO: Created or updated team object
            
        Raises:
            HTTPException: If user not found, not a member, or drivers not unique
        """
        # Verify user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Verify user is a member of this league
        membership = self.session.exec(
            select(UserLeagueLink).where(
                UserLeagueLink.league_id == league_id,
                UserLeagueLink.user_id == user.id,
                UserLeagueLink.is_active == True
            )
        ).first()
        
        if not membership:
            raise HTTPException(status_code=403, detail="Access denied: You are not a member of this league")
        
        # Validate drivers are unique (using domain service)
        try:
            self.validation_service.validate_unique_drivers(
                team_data.driver_1_id,
                team_data.driver_2_id,
                team_data.driver_3_id
            )
        except DuplicateDriverError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        
        # Calculate budget remaining (using domain service)
        try:
            budget_remaining = self.budget_service.calculate_remaining_budget(
                team_data.driver_1_id,
                team_data.driver_2_id,
                team_data.driver_3_id,
                team_data.constructor_id
            )
        except DriverNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except ConstructorNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except BudgetExceededError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        
        # Check if user already has a team in this league
        existing_team = self.user_teams_repo.get_by_league_and_user(league_id, user.id)
        
        if existing_team:
            # Update existing team
            updated_team = self.user_teams_repo.update(
                existing_team.id,
                UserTeamUpdateDTO(
                    team_name=team_data.team_name,
                    driver_1_id=team_data.driver_1_id,
                    driver_2_id=team_data.driver_2_id,
                    driver_3_id=team_data.driver_3_id,
                    constructor_id=team_data.constructor_id,
                    budget_remaining=budget_remaining
                )
            )
            self.session.commit()
            
            return UserTeamMapper.to_response_dto(updated_team)
        else:
            # Create new team
            new_team = self.user_teams_repo.create(
                UserTeamCreateDTO(
                    user_id=user.id,
                    league_id=league_id,
                    team_name=team_data.team_name,
                    driver_1_id=team_data.driver_1_id,
                    driver_2_id=team_data.driver_2_id,
                    driver_3_id=team_data.driver_3_id,
                    constructor_id=team_data.constructor_id,
                    budget_remaining=budget_remaining
                )
            )
            self.session.commit()
            
            return UserTeamMapper.to_response_dto(new_team)


class GetMyTeamService:
    """
    Service for retrieving a user's team in a specific league
    Business logic:
    - Validates user exists
    - Returns team or None if no team exists
    """
    
    def __init__(
        self,
        user_teams_repo: UserTeamsRepository,
        user_repo: UserRepository
    ):
        self.user_teams_repo = user_teams_repo
        self.user_repo = user_repo
    
    def execute(self, league_id: int, user_id: str) -> UserTeamResponseDTO | None:
        """
        Get the current user's team in a specific league
        
        Args:
            league_id: ID of the league to get team from
            user_id: Supabase user ID of the team owner
            
        Returns:
            UserTeamResponseDTO | None: User's team in the league or None if no team exists
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get user's team in this league
        team = self.user_teams_repo.get_by_league_and_user(league_id, user.id)
        
        if not team:
            return None
        
        return UserTeamMapper.to_response_dto(team)


class GetAllMyTeamsService:
    """
    Service for retrieving ALL user teams across all leagues
    Business logic:
    - Validates user exists
    - Returns list of teams with league and driver details
    """
    
    def __init__(
        self,
        session: Session,
        user_repo: UserRepository
    ):
        self.session = session
        self.user_repo = user_repo
        self.enrichment_service = TeamEnrichmentService(session)
    
    def execute(self, user_id: str) -> list[dict]:
        """
        Get all teams belonging to the current user across all leagues
        
        Args:
            user_id: Supabase user ID of the team owner
            
        Returns:
            list[dict]: List of team data with detailed information including
                       league name, drivers with headshos, and constructor details
            
        Raises:
            HTTPException: If user not found
        """
        # Verify user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get all user's active teams
        user_teams = self.session.exec(
            select(UserTeams).where(
                UserTeams.user_id == user.id,
                UserTeams.is_active == True
            )
        ).all()
        
        # Enrich teams with related data using enrichment service
        return [self.enrichment_service.enrich_team_data(team) for team in user_teams]


class SwapReserveDriverService:
    """
    Service for swapping a main driver with the reserve driver
    Business logic:
    - Validates team exists
    - Identifies which slot the driver is in (using domain service)
    - Swaps driver with reserve
    """
    
    def __init__(
        self,
        session: Session,
        user_teams_repo: UserTeamsRepository
    ):
        self.session = session
        self.user_teams_repo = user_teams_repo
        self.validation_service = TeamValidationService()
    
    def execute(self, user_id: int, driver_id: int, league_id: int) -> dict:
        """
        Swap a main driver with the reserve driver
        The specified driver_id will become the reserve, and the current reserve will take its slot
        
        Args:
            user_id: Internal user ID (not Supabase ID)
            driver_id: ID of the driver to make reserve (currently in slot 1, 2, or 3)
            league_id: League ID
            
        Returns:
            dict with success status, message, and updated team configuration
            
        Raises:
            HTTPException: If team not found or driver not in team
        """
        # Get user's team
        team = self.session.exec(
            select(UserTeams).where(
                UserTeams.user_id == user_id,
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
        
        if not team:
            raise HTTPException(404, "Team not found")
        
        # Validate driver is in team and get slot (using domain service)
        try:
            driver_slot = self.validation_service.validate_driver_in_team(
                driver_id,
                team.driver_1_id,
                team.driver_2_id,
                team.driver_3_id,
                team.reserve_driver_id
            )
        except DriverAlreadyReserveError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        except DriverNotInTeamError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e
        
        # Swap drivers
        current_reserve = team.reserve_driver_id
        
        if driver_slot == 1:
            team.driver_1_id = current_reserve
        elif driver_slot == 2:
            team.driver_2_id = current_reserve
        elif driver_slot == 3:
            team.driver_3_id = current_reserve
        
        team.reserve_driver_id = driver_id
        team.updated_at = datetime.now()
        
        self.session.add(team)
        self.session.commit()
        
        return {
            "success": True,
            "message": "Reserve driver swapped successfully",
            "team": {
                "driver_1_id": team.driver_1_id,
                "driver_2_id": team.driver_2_id,
                "driver_3_id": team.driver_3_id,
                "reserve_driver_id": team.reserve_driver_id
            }
        }
