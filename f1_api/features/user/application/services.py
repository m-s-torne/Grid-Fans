"""User application services - Business logic and use cases"""
from fastapi import HTTPException
from ..domain.interfaces import UserRepository
from ..domain.models import UserCreate
from ..application.dtos import UserCreateDTO, UserResponseDTO


class CreateUserService:
    """Service for creating new users
    
    This encapsulates the business logic for user creation:
    - Validates that user doesn't already exist
    - Creates the user in the database
    - Returns standardized response
    """
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def execute(self, user_data: UserCreateDTO) -> UserResponseDTO:
        """
        Create a new user with Supabase integration
        
        Args:
            user_data: UserCreateDTO with user information
            
        Returns:
            UserResponseDTO: Created user data
            
        Raises:
            HTTPException: If user already exists
        """
        # Business rule: Check if user already exists
        user_create = UserCreate(
            user_name=user_data.user_name,
            email=user_data.email,
            supabase_user_id=user_data.supabase_user_id
        )
        
        existing = self.repository.get_existing_user(user_create)
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Username, email, or Supabase user already registered"
            )
        
        # Create the user
        new_user = self.repository.create(user_create)
        
        # Return DTO
        return UserResponseDTO(
            id=new_user.id,
            user_name=new_user.user_name,
            email=new_user.email,
            is_verified=new_user.is_verified,
            created_at=new_user.created_at
        )


class GetUserService:
    """Service for retrieving user information"""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    def get_by_supabase_id(self, supabase_user_id: str) -> UserResponseDTO:
        """Get user by Supabase ID
        
        Args:
            supabase_user_id: Supabase user identifier
            
        Returns:
            UserResponseDTO: User data
            
        Raises:
            HTTPException: If user not found
        """
        user = self.repository.get_by_supabase_id(supabase_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return UserResponseDTO(
            id=user.id,
            user_name=user.user_name,
            email=user.email,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
