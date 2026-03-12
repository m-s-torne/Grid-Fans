"""User repository contract - Abstract interface for data access"""
from typing import Protocol
from .models import Users, UserCreate


class UserRepository(Protocol):
    """Abstract repository interface for User entity.
    
    This defines the contract that infrastructure layer must implement.
    Following Dependency Inversion Principle - domain defines the contract.
    """
    
    def get_by_id(self, user_id: int) -> Users | None:
        """Get user by internal ID"""
        ...
    
    def get_by_supabase_id(self, supabase_user_id: str) -> Users | None:
        """Get user by Supabase user ID"""
        ...
    
    def get_by_email(self, email: str) -> Users | None:
        """Get user by email"""
        ...
    
    def get_by_username(self, username: str) -> Users | None:
        """Get user by username"""
        ...
    
    def get_existing_user(self, user_data: UserCreate) -> Users | None:
        """Check if user already exists (by username, email, or supabase_id)"""
        ...
    
    def create(self, user_data: UserCreate) -> Users:
        """Create a new user"""
        ...
    
    def save(self, user: Users) -> Users:
        """Save or update user"""
        ...

    def get_users_names_by_ids(self, user_ids: list[int]) -> dict[int, str]:
        """Get a mapping of user_id -> user_name for a list of user IDs"""
        ...
