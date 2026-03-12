from f1_api.core.f1_data.domain.models import Seasons, Events, Sessions, SessionResult
from f1_api.features.teams.domain.models import Teams
from f1_api.features.drivers.domain.models import Drivers, DriverTeamLink

from f1_api.features.user.domain.models import (
    Users,
    UserCreate,
    UserResponse
)

from f1_api.features.leagues.domain.models import (
    Leagues,
    UserLeagueLink,
    LeagueCreate,
    LeagueResponse,
    LeagueJoin
)

from f1_api.features.user_teams.domain.models import UserTeams
from f1_api.features.user_teams.application.dtos import (
    UserTeamCreateDTO as UserTeamsCreate,
    UserTeamUpdateDTO as UserTeamUpdate,
    UserTeamResponseDTO as UserTeamResponse
)

__all__ = [
    # F1 Schemas
    "Seasons",
    "Events",
    "Sessions",
    "Teams",
    "Drivers",
    "DriverTeamLink",
    "SessionResult",
    # App Models
    "Leagues",
    "Users",
    "UserLeagueLink",
    "UserTeams",
    "UserTeamsCreate",
    "UserTeamUpdate",
    "UserTeamResponse",
    "UserCreate",
    "UserResponse",
    "LeagueCreate",
    "LeagueResponse",
    "LeagueJoin",
]
