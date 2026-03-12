"""User repository implementation - Concrete database access using SQLModel"""
from sqlmodel import Session, select, col
from ..domain.models import Users, UserCreate
from ..domain.interfaces import UserRepository as IUserRepository


class UserRepositoryImpl(IUserRepository):
    """SQLModel implementation of UserRepository
    
    This implements the domain repository contract using SQLModel directly.
    All data access logic is self-contained without legacy dependencies.
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, user_id: int) -> Users | None:
        """Get user by internal ID"""
        return self.session.get(Users, user_id)
    
    def get_by_supabase_id(self, supabase_user_id: str) -> Users | None:
        """Get user by Supabase user ID"""
        return self.session.exec(
            select(Users).where(Users.supabase_user_id == supabase_user_id)
        ).first()
    
    def get_by_email(self, email: str) -> Users | None:
        """Get user by email"""
        return self.session.exec(
            select(Users).where(Users.email == email)
        ).first()
    
    def get_by_username(self, username: str) -> Users | None:
        """Get user by username"""
        return self.session.exec(
            select(Users).where(Users.user_name == username)
        ).first()
    
    def get_existing_user(self, user_data: UserCreate) -> Users | None:
        """Check if user already exists by username, email, or supabase_id"""
        return self.session.exec(
            select(Users).where(
                (Users.user_name == user_data.user_name) |
                (Users.email == user_data.email) |
                (Users.supabase_user_id == user_data.supabase_user_id)
            )
        ).first()
    
    def create(self, user_data: UserCreate) -> Users:
        """Create and persist a new user"""
        new_user = Users(
            user_name=user_data.user_name,
            email=user_data.email,
            supabase_user_id=user_data.supabase_user_id,
            is_verified=True
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def save(self, user: Users) -> Users:
        """Save or update user"""
        self.session.add(user)
        self.session.flush()
        return user

    def get_users_names_by_ids(self, user_ids: list[int]) -> dict[int, str]:
        """Get a mapping of user_id -> user_name for a list of user IDs."""
        if not user_ids:
            return {}
        users_list = self.session.exec(
            select(Users).where(col(Users.id).in_(user_ids))
        ).all()
        return {u.id: u.user_name for u in users_list}
