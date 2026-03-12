"""User presentation layer - HTTP endpoints and routes"""
from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..application.services import CreateUserService, GetUserService
from ..application.dtos import UserCreateDTO, UserResponseDTO
from ..infrastructure.repositories import UserRepositoryImpl
from f1_api.dependencies import get_db_session
from f1_api.features.user_teams.application.services import GetAllMyTeamsService

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponseDTO)
def create_user(
    user_data: UserCreateDTO,
    session: Session = Depends(get_db_session)
) -> UserResponseDTO:
    """Create a new user with Supabase integration
    
    This endpoint follows DDD principles:
    1. Presentation layer receives HTTP request
    2. Infrastructure layer provides repository implementation
    3. Application layer executes business logic
    4. Returns DTO as response
    """
    repository = UserRepositoryImpl(session)
    service = CreateUserService(repository)
    return service.execute(user_data)


@router.get("/by-id/{supabase_user_id}", response_model=UserResponseDTO)
def get_user_by_id(
    supabase_user_id: str,
    session: Session = Depends(get_db_session)
) -> UserResponseDTO:
    """Get the user from the database by Supabase ID"""
    repository = UserRepositoryImpl(session)
    service = GetUserService(repository)
    return service.get_by_supabase_id(supabase_user_id)


@router.get("/my-teams")
def get_my_teams(
    user_id: str,
    session: Session = Depends(get_db_session)
):
    """
    Get all teams belonging to the current user across all leagues
    
    Returns enriched team data including:
    - League name
    - Driver details with headshots
    - Constructor details with logo
    """
    user_repo = UserRepositoryImpl(session)
    service = GetAllMyTeamsService(session, user_repo)
    return service.execute(user_id)
