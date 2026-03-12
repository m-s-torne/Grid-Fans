"""League repository implementations - Concrete database access"""
from sqlmodel import Session, select
from ..domain.models import Leagues, UserLeagueLink, LeagueCreate
from ..domain.interfaces import LeagueRepository as ILeagueRepository
from ..domain.interfaces import UserLeagueLinkRepository as IUserLeagueLinkRepository
from f1_api.features.user.domain.models import Users


class LeagueRepositoryImpl(ILeagueRepository):
    """SQLModel implementation of LeagueRepository - Fully autonomous, no legacy dependencies"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_id(self, league_id: int) -> Leagues | None:
        """Get league by ID"""
        return self.session.exec(
            select(Leagues).where(Leagues.id == league_id)
        ).first()
    
    def get_by_join_code(self, join_code: str) -> Leagues | None:
        """Get active league by join code"""
        return self.session.exec(
            select(Leagues).where(
                Leagues.join_code == join_code,
                Leagues.is_active == True
            )
        ).first()
    
    def create(self, league_data: LeagueCreate, admin_user_id: int, join_code: str) -> Leagues:
        """Create new league"""
        new_league = Leagues(
            name=league_data.name,
            description=league_data.description,
            admin_user_id=admin_user_id,
            join_code=join_code,
            is_active=True
        )
        self.session.add(new_league)
        self.session.commit()
        self.session.refresh(new_league)
        return new_league
    
    def get_all(self) -> list[Leagues]:
        """Get all leagues"""
        return self.session.exec(select(Leagues)).all()
    
    def get_user_leagues(self, user_id: int) -> list[Leagues]:
        """Get all active leagues for a user"""
        statement = (
            select(Leagues)
            .join(UserLeagueLink)
            .where(UserLeagueLink.user_id == user_id)
            .where(UserLeagueLink.is_active == True)
        )
        return self.session.exec(statement).all()
    
    def count_participants(self, league_id: int) -> int:
        """Count active participants in a league"""
        statement = (
            select(UserLeagueLink)
            .where(UserLeagueLink.league_id == league_id)
            .where(UserLeagueLink.is_active == True)
        )
        return len(self.session.exec(statement).all())


class UserLeagueLinkRepositoryImpl(IUserLeagueLinkRepository):
    """SQLModel implementation of UserLeagueLinkRepository - Fully autonomous, no legacy dependencies"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def get_membership(self, user_id: int, league_id: int) -> UserLeagueLink | None:
        """Get membership (active or inactive) for a user in a league"""
        return self.session.exec(
            select(UserLeagueLink).where(
                UserLeagueLink.league_id == league_id,
                UserLeagueLink.user_id == user_id
            )
        ).first()
    
    def create_membership(self, user_id: int, league_id: int, is_admin: bool = False) -> UserLeagueLink:
        """Create new membership relationship between user and league"""
        league_link = UserLeagueLink(
            user_id=user_id,
            league_id=league_id,
            is_admin=is_admin,
            is_active=True
        )
        self.session.add(league_link)
        self.session.commit()
        self.session.refresh(league_link)
        return league_link
    
    def activate_membership(self, user_id: int, league_id: int) -> UserLeagueLink:
        """Reactivate an existing inactive membership"""
        membership = self.get_membership(user_id, league_id)
        if not membership:
            raise ValueError(f"No membership found for user {user_id} in league {league_id}")
        
        membership.is_active = True
        self.session.add(membership)
        self.session.commit()
        self.session.refresh(membership)
        return membership
    
    def deactivate_membership(self, user_id: int, league_id: int) -> bool:
        """Deactivate an existing active membership"""
        membership = self.get_membership(user_id, league_id)
        if membership and membership.is_active:
            membership.is_active = False
            self.session.add(membership)
            self.session.commit()
            return True
        return False
    
    def is_user_member(self, user_id: int, league_id: int) -> bool:
        """Check if user has active membership in league"""
        membership = self.session.exec(
            select(UserLeagueLink).where(
                UserLeagueLink.league_id == league_id,
                UserLeagueLink.user_id == user_id,
                UserLeagueLink.is_active == True
            )
        ).first()
        return membership is not None
    
    def is_user_admin(self, user_id: int, league_id: int) -> bool:
        """Check if user is an admin in league"""
        membership = self.session.exec(
            select(UserLeagueLink).where(
                UserLeagueLink.league_id == league_id,
                UserLeagueLink.user_id == user_id,
                UserLeagueLink.is_active == True
            )
        ).first()
        return membership is not None and membership.is_admin
    
    def get_league_participants(self, league_id: int) -> list:
        """Get all active participants in a league with user details
        
        Returns:
            list[tuple[Users, UserLeagueLink]]: List of (user, membership) tuples
        """
        participants_query = (
            select(Users, UserLeagueLink)
            .join(UserLeagueLink, Users.id == UserLeagueLink.user_id)
            .where(
                UserLeagueLink.league_id == league_id,
                UserLeagueLink.is_active == True
            )
        )
        return self.session.exec(participants_query).all()
