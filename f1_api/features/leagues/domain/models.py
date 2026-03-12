from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField
from datetime import datetime


class Leagues(SQLModel, table=True):
    id: int = SQLField(default=None, primary_key=True)
    name: str
    description: str | None = None
    admin_user_id: int = SQLField(foreign_key="users.id")
    is_active: bool = SQLField(default=True)
    join_code: str = SQLField(unique=True, index=True)
    created_at: datetime = SQLField(default_factory=datetime.now)


class UserLeagueLink(SQLModel, table=True):
    user_id: int = SQLField(foreign_key="users.id", primary_key=True)
    league_id: int = SQLField(foreign_key="leagues.id", primary_key=True)
    is_admin: bool = SQLField(default=False)
    is_active: bool = SQLField(default=True)
    joined_at: datetime = SQLField(default_factory=datetime.now)


class LeagueCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class LeagueResponse(BaseModel):
    id: int
    name: str
    description: str | None
    admin_user_id: int
    is_active: bool
    join_code: str
    current_participants: int
    created_at: datetime


class LeagueJoin(BaseModel):
    join_code: str = Field(min_length=6, max_length=10)
