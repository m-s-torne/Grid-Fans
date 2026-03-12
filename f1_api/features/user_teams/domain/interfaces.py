"""User Teams domain interfaces - Repository contracts"""
from typing import Protocol
from .models import UserTeams


class UserTeamsRepository(Protocol):
    """Repository interface for User Teams operations"""
    
    def get_by_id(self, team_id: int) -> UserTeams | None:
        """Get a user team by ID"""
        ...
    
    def get_by_league_and_user(self, league_id: int, user_id: int) -> UserTeams | None:
        """Get active team for a user in a specific league"""
        ...
    
    def has_active_team(self, user_id: int, league_id: int) -> bool:
        """Check if user has an active team in a league"""
        ...
    
    def create(self, team: UserTeams) -> UserTeams:
        """Create a new user team"""
        ...
    
    def update(self, team: UserTeams) -> UserTeams:
        """Update an existing user team"""
        ...
    
    def soft_delete(self, team: UserTeams) -> None:
        """Soft delete a team (set is_active=False)"""
        ...
    
    def hard_delete(self, team_id: int) -> bool:
        """Hard delete a team from database"""
        ...
