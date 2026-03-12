"""
User Teams Infrastructure Layer - Repository Implementation
Concrete implementation of UserTeamsRepository Protocol
"""
import logging
from datetime import datetime
from sqlmodel import Session, select

from ..domain.models import UserTeams
from ..domain.interfaces import UserTeamsRepository
from ..application.dtos import UserTeamCreateDTO, UserTeamUpdateDTO

logger = logging.getLogger(__name__)


class UserTeamsRepositoryImpl(UserTeamsRepository):
    """Concrete implementation of UserTeamsRepository using SQLModel"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, team_id: int) -> UserTeams | None:
        """
        Get a user team by its ID
        
        Args:
            team_id: ID of the team
            
        Returns:
            UserTeams | None: Team object or None if not found
        """
        return self.session.exec(
            select(UserTeams).where(UserTeams.id == team_id)
        ).first()
    
    def get_by_league_and_user(self, league_id: int, user_id: int) -> UserTeams | None:
        """
        Get a user's active team in a specific league
        
        Args:
            league_id: ID of the league
            user_id: Internal user ID (not Supabase ID)
            
        Returns:
            UserTeams | None: Team object or None if not found
        """
        return self.session.exec(
            select(UserTeams).where(
                UserTeams.user_id == user_id,
                UserTeams.league_id == league_id,
                UserTeams.is_active == True
            )
        ).first()
    
    def has_active_team(self, league_id: int, user_id: int) -> bool:
        """
        Check if a user has an active team in a league
        
        Args:
            league_id: ID of the league
            user_id: Internal user ID
            
        Returns:
            bool: True if user has active team, False otherwise
        """
        team = self.get_by_league_and_user(league_id, user_id)
        return team is not None
    
    def create(self, team_data: UserTeamCreateDTO) -> UserTeams:
        """
        Create a new user team
        
        Args:
            team_data: UserTeamCreateDTO with team data
            
        Returns:
            UserTeams: Created team object
        """
        new_team = UserTeams(
            user_id=team_data.user_id,
            league_id=team_data.league_id,
            team_name=team_data.team_name,
            driver_1_id=team_data.driver_1_id,
            driver_2_id=team_data.driver_2_id,
            driver_3_id=team_data.driver_3_id,
            reserve_driver_id=team_data.reserve_driver_id,
            constructor_id=team_data.constructor_id,
            total_points=0,
            budget_remaining=team_data.budget_remaining,
            is_active=True
        )
        
        self.session.add(new_team)
        self.session.flush()  # Flush to get the ID
        
        logger.info(f"Created user team {new_team.id} for user {team_data.user_id} in league {team_data.league_id}")
        
        return new_team
    
    def update(self, team_id: int, team_data: UserTeamUpdateDTO) -> UserTeams:
        """
        Update an existing user team
        
        Args:
            team_id: ID of the team to update
            team_data: UserTeamUpdateDTO with updated data
            
        Returns:
            UserTeams: Updated team object
            
        Raises:
            ValueError: If team not found
        """
        team = self.get_by_id(team_id)
        
        if not team:
            raise ValueError(f"Team with ID {team_id} not found")
        
        # Update fields if provided
        if team_data.team_name is not None:
            team.team_name = team_data.team_name
        
        if team_data.driver_1_id is not None:
            team.driver_1_id = team_data.driver_1_id
        
        if team_data.driver_2_id is not None:
            team.driver_2_id = team_data.driver_2_id
        
        if team_data.driver_3_id is not None:
            team.driver_3_id = team_data.driver_3_id
        
        if team_data.constructor_id is not None:
            team.constructor_id = team_data.constructor_id
        
        if team_data.budget_remaining is not None:
            team.budget_remaining = team_data.budget_remaining
        
        team.updated_at = datetime.now()
        
        self.session.add(team)
        
        logger.info(f"Updated user team {team_id}")
        
        return team
    
    def soft_delete(self, team_id: int) -> bool:
        """
        Soft delete a user team (set is_active to False)
        
        Args:
            team_id: ID of the team to soft delete
            
        Returns:
            bool: True if team was deleted, False if not found
        """
        team = self.get_by_id(team_id)
        
        if not team:
            logger.warning(f"Attempted to soft delete non-existent team {team_id}")
            return False
        
        team.is_active = False
        team.updated_at = datetime.now()
        
        self.session.add(team)
        
        logger.info(f"Soft deleted user team {team_id}")
        
        return True
    
    def hard_delete(self, team_id: int) -> bool:
        """
        Hard delete a user team (permanently remove from database)
        
        Args:
            team_id: ID of the team to hard delete
            
        Returns:
            bool: True if team was deleted, False if not found
        """
        team = self.get_by_id(team_id)
        
        if not team:
            logger.warning(f"Attempted to hard delete non-existent team {team_id}")
            return False
        
        self.session.delete(team)
        
        logger.info(f"Hard deleted user team {team_id}")
        
        return True
