"""League repository contracts - Abstract interfaces for data access"""
from typing import Protocol, Any
from ..domain.models import Leagues, UserLeagueLink, LeagueCreate


class LeagueRepository(Protocol):
    """Abstract repository interface for League entity"""
    
    def get_by_id(self, league_id: int) -> Leagues | None:
        """Get league by ID"""
        ...
    
    def get_by_join_code(self, join_code: str) -> Leagues | None:
        """Get league by join code"""
        ...
    
    def create(self, league_data: LeagueCreate, admin_user_id: int, join_code: str) -> Leagues:
        """Create a new league"""
        ...
    
    def get_all(self) -> list[Leagues]:
        """Get all leagues"""
        ...
    
    def get_user_leagues(self, user_id: int) -> list[Leagues]:
        """Get all leagues a user belongs to"""
        ...
    
    def count_participants(self, league_id: int) -> int:
        """Count active participants in a league"""
        ...


class UserLeagueLinkRepository(Protocol):
    """Abstract repository interface for UserLeagueLink entity"""
    
    def get_membership(self, user_id: int, league_id: int) -> UserLeagueLink | None:
        """Get user's membership in a league"""
        ...
    
    def create_membership(self, user_id: int, league_id: int, is_admin: bool = False) -> UserLeagueLink:
        """Create a new user-league membership"""
        ...
    
    def activate_membership(self, user_id: int, league_id: int) -> UserLeagueLink:
        """Activate an existing membership"""
        ...
    
    def deactivate_membership(self, user_id: int, league_id: int) -> bool:
        """Deactivate a membership"""
        ...
    
    def is_user_member(self, user_id: int, league_id: int) -> bool:
        """Check if user is an active member"""
        ...
    
    def is_user_admin(self, user_id: int, league_id: int) -> bool:
        """Check if user is an admin of the league"""
        ...
    
    def get_league_participants(self, league_id: int) -> list[tuple[Any, UserLeagueLink]]:
        """Get all active participants in a league with user details
        
        Returns:
            list[tuple[Users, UserLeagueLink]]: List of (user, membership) tuples
        """
        ...


class IInitializeLeagueOwnershipUseCase(Protocol):
    """Protocol for initializing driver ownership records for a newly created league."""

    def execute(self, league_id: int, season: int) -> int: ...


class IInitializeUserTeamUseCase(Protocol):
    """Protocol for initializing a user's team when they join a league."""

    def execute(self, user_id: int, league_id: int) -> dict: ...
