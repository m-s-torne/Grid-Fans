"""League application services - Business logic and use cases"""
import logging
import random
import string
from fastapi import HTTPException
from sqlmodel import Session
from ..domain.interfaces import LeagueRepository, UserLeagueLinkRepository, IInitializeLeagueOwnershipUseCase, IInitializeUserTeamUseCase
from ..domain.models import LeagueCreate
from ..application.dtos import LeagueCreateDTO, LeagueResponseDTO, LeagueJoinDTO, LeagueListItemDTO
from f1_api.features.user.domain.interfaces import UserRepository
from f1_api.features.user_teams.infrastructure.repositories import UserTeamsRepositoryImpl


class CreateLeagueService:
    """Service for creating new leagues
    
    Business logic:
    - Validates user exists
    - Generates unique join code
    - Creates league
    - Adds creator as admin member
    - Initializes driver ownership for league
    - Optionally initializes team for creator
    """
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        user_repo: UserRepository,
        membership_repo: UserLeagueLinkRepository,
        session: Session,
        initialize_ownership: IInitializeLeagueOwnershipUseCase | None = None,
        initialize_user_team: IInitializeUserTeamUseCase | None = None,
    ):
        self.league_repo = league_repo
        self.user_repo = user_repo
        self.membership_repo = membership_repo
        self.session = session
        self.initialize_ownership = initialize_ownership
        self.initialize_user_team = initialize_user_team
    
    def execute(self, user_id: str, league_data: LeagueCreateDTO) -> LeagueResponseDTO:
        """Create a new league
        
        Args:
            user_id: Supabase user ID
            league_data: League creation data
            
        Returns:
            LeagueResponseDTO with league information
            
        Raises:
            HTTPException: If user not found
        """
        # Validate user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate unique join code (domain logic delegated to repository)
        league_create = LeagueCreate(
            name=league_data.name,
            description=league_data.description
        )

        # Create league with generated join code
        # Note: join_code generation moved to repository/infrastructure
        join_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        new_league = self.league_repo.create(league_create, user.id, join_code)
        
        # Create admin membership
        self.membership_repo.create_membership(user.id, new_league.id, is_admin=True)
        
        # Commit league and membership creation
        self.session.commit()
        
        # Initialize driver ownership for the league (CRITICAL - must succeed)
        current_season = 2025  # hardcoded until season config service is available
        assert self.initialize_ownership is not None, "initialize_ownership use case is required"
        try:
            drivers_initialized = self.initialize_ownership.execute(new_league.id, current_season)
            self.session.commit()  # Commit driver ownership records
            logging.info("Initialized %d drivers for league %d", drivers_initialized, new_league.id)
        except Exception as e:
            self.session.rollback()
            logging.error("CRITICAL: Failed to initialize driver ownership for league %d: %s", new_league.id, str(e))
            raise HTTPException(status_code=500, detail=f"Failed to initialize drivers: {str(e)}") from e

        # Initialize team for the league creator automatically (CRITICAL - must succeed)
        assert self.initialize_user_team is not None, "initialize_user_team use case is required"
        try:
            self.initialize_user_team.execute(user.id, new_league.id)
            self.session.commit()  # Commit team initialization
            logging.info("Initialized team for league creator %d in league %d", user.id, new_league.id)
        except HTTPException:
            # Re-raise HTTP exceptions (400, 500)
            self.session.rollback()
            logging.error("Failed to initialize team for league creator %d", user.id)
            raise
        except Exception as e:
            self.session.rollback()
            logging.error("Unexpected error initializing team for league creator %d: %s", user.id, str(e))
            raise HTTPException(status_code=500, detail=f"Failed to initialize team: {str(e)}") from e
        
        # Count participants (should be 1 - just the creator)
        participant_count = self.league_repo.count_participants(new_league.id)
        
        return LeagueResponseDTO(
            id=new_league.id,
            name=new_league.name,
            description=new_league.description,
            admin_user_id=new_league.admin_user_id,
            is_active=new_league.is_active,
            join_code=new_league.join_code,
            current_participants=participant_count,
            created_at=new_league.created_at
        )


class JoinLeagueService:
    """Service for users joining existing leagues"""
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        user_repo: UserRepository,
        membership_repo: UserLeagueLinkRepository,
        session: Session,
        initialize_user_team: IInitializeUserTeamUseCase | None = None,
    ):
        self.league_repo = league_repo
        self.user_repo = user_repo
        self.membership_repo = membership_repo
        self.session = session
        self.initialize_user_team = initialize_user_team
    
    def execute(self, user_id: str, join_data: LeagueJoinDTO) -> dict:
        """Join a league using join code
        
        Args:
            user_id: Supabase user ID
            join_data: Join code information
            
        Returns:
            dict with success status and league info
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate user
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Find league by join code
        league = self.league_repo.get_by_join_code(join_data.join_code)
        if not league:
            raise HTTPException(status_code=404, detail="League not found with that join code")
        
        # Check if already a member
        existing_membership = self.membership_repo.get_membership(user.id, league.id)
        
        if existing_membership:
            if existing_membership.is_active:
                raise HTTPException(status_code=400, detail="You are already a member of this league")
            else:
                # Reactivate membership
                self.membership_repo.activate_membership(user.id, league.id)
                is_rejoining = True
        else:
            # Create new membership
            self.membership_repo.create_membership(user.id, league.id, is_admin=False)
            is_rejoining = False
        
        # Commit membership creation
        self.session.commit()
        
        # Initialize team for new members
        team_init_result = None
        if not is_rejoining and self.initialize_user_team is not None:
            try:
                team_init_result = self.initialize_user_team.execute(user.id, league.id)
                self.session.commit()  # Commit team initialization
                logging.info("Initialized team for user %d in league %d", user.id, league.id)
            except Exception as e:  # noqa: BLE001  # pylint: disable=broad-except
                self.session.rollback()
                logging.error("Failed to initialize team for user %d: %s", user.id, str(e))
                team_init_result = {"error": str(e)}
        
        return {
            "success": True,
            "message": "Rejoined league successfully" if is_rejoining else "Joined league successfully",
            "league_id": league.id,
            "league_name": league.name,
            "team_initialized": team_init_result is not None and "error" not in team_init_result,
            "team_details": team_init_result
        }


class GetUserLeaguesService:
    """Service for retrieving user's leagues"""
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        user_repo: UserRepository,
        membership_repo: UserLeagueLinkRepository
    ):
        self.league_repo = league_repo
        self.user_repo = user_repo
        self.membership_repo = membership_repo
    
    def execute(self, user_id: str) -> list[LeagueListItemDTO]:
        """Get all leagues for a user
        
        Args:
            user_id: Supabase user ID
            
        Returns:
            List of LeagueListItemDTO
        """
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        leagues = self.league_repo.get_user_leagues(user.id)
        
        result = []
        for league in leagues:
            is_admin = self.membership_repo.is_user_admin(user.id, league.id)
            participant_count = self.league_repo.count_participants(league.id)
            
            result.append(LeagueListItemDTO(
                id=league.id,
                name=league.name,
                description=league.description,
                is_admin=is_admin,
                current_participants=participant_count,
                created_at=league.created_at
            ))
        
        return result


class GetLeagueDetailsService:
    """Service for retrieving detailed information about a specific league"""
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        user_repo: UserRepository,
        membership_repo: UserLeagueLinkRepository
    ):
        self.league_repo = league_repo
        self.user_repo = user_repo
        self.membership_repo = membership_repo
    
    def execute(self, league_id: int, user_id: str) -> LeagueResponseDTO:
        """Get league details - only for league participants
        
        Args:
            league_id: ID of the league
            user_id: Supabase user ID
            
        Returns:
            LeagueResponseDTO with league details
            
        Raises:
            HTTPException: If user not found, not a participant, or league not found
        """
        # Validate user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get league
        league = self.league_repo.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")
        
        # Check if user is a participant
        membership = self.membership_repo.get_membership(user.id, league_id)
        if not membership or not membership.is_active:
            raise HTTPException(status_code=403, detail="Access denied: You are not a member of this league")
        
        # Get participant count
        participant_count = self.league_repo.count_participants(league_id)
        
        return LeagueResponseDTO(
            id=league.id,
            name=league.name,
            description=league.description,
            admin_user_id=league.admin_user_id,
            is_active=league.is_active,
            join_code=league.join_code,
            current_participants=participant_count,
            created_at=league.created_at
        )


class GetLeagueParticipantsService:
    """Service for retrieving all participants in a league"""
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        membership_repo: UserLeagueLinkRepository
    ):
        self.league_repo = league_repo
        self.membership_repo = membership_repo
    
    def execute(self, league_id: int) -> dict:
        """Get all participants of a league
        
        Args:
            league_id: ID of the league
            
        Returns:
            Dict with league info and participants list
            
        Raises:
            HTTPException: If league not found
        """
        # Verify league exists
        league = self.league_repo.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")
        
        # Get all active memberships (returns tuples of (User, UserLeagueLink))
        participants_data = self.membership_repo.get_league_participants(league_id)
        
        participants = [
            {
                "user_id": user.id,
                "user_name": user.user_name,
                "email": user.email,
                "is_admin": membership.is_admin,
                "joined_at": membership.joined_at
            }
            for user, membership in participants_data
        ]
        
        return {
            "league_id": league_id,
            "league_name": league.name,
            "participants": participants,
            "total_participants": len(participants)
        }


class LeaveLeagueService:
    """Service for leaving a league
    
    Business logic:
    - Validates user exists
    - Validates league exists
    - Validates user is a member
    - Deactivates membership
    - Deletes user's team in the league
    """
    
    def __init__(
        self,
        league_repo: LeagueRepository,
        user_repo: UserRepository,
        membership_repo: UserLeagueLinkRepository,
        session: Session
    ):
        self.league_repo = league_repo
        self.user_repo = user_repo
        self.membership_repo = membership_repo
        self.session = session
    
    def execute(self, league_id: int, user_id: str) -> dict:
        """Remove user from a league and delete their team
        
        Args:
            league_id: ID of the league to leave
            user_id: Supabase user ID of the user leaving
            
        Returns:
            Dict with success message and league info
            
        Raises:
            HTTPException: If user not found, league not found, or user not a member
        """
        # Validate user exists
        user = self.user_repo.get_by_supabase_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate league exists
        league = self.league_repo.get_by_id(league_id)
        if not league:
            raise HTTPException(status_code=404, detail="League not found")
        
        # Validate user is a member
        membership = self.membership_repo.get_membership(user.id, league_id)
        if not membership or not membership.is_active:
            raise HTTPException(status_code=404, detail="User is not a member of this league")
        
        # Deactivate membership
        self.membership_repo.deactivate_membership(user.id, league_id)
        
        # Delete user's team in the league
        user_teams_repo = UserTeamsRepositoryImpl(self.session)
        team = user_teams_repo.get_by_league_and_user(league_id, user.id)
        if team:
            user_teams_repo.hard_delete(team.id)
        
        # Commit changes
        self.session.commit()
        
        return {
            "message": f"Successfully left league '{league.name}'",
            "league_id": league_id
        }
