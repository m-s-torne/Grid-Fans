"""User Teams domain models - Core business entities"""
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field
from datetime import datetime


class UserTeams(SQLModel, table=True):
    """User Team entity - Represents a user's fantasy team in a league
    
    A user team consists of 3 main drivers, 1 reserve driver, and a constructor.
    Each user can have one active team per league.
    """
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    league_id: int = Field(foreign_key="leagues.id")
    team_name: str
    driver_1_id: int = Field(foreign_key="drivers.id")
    driver_2_id: int = Field(foreign_key="drivers.id")
    driver_3_id: int = Field(foreign_key="drivers.id")
    reserve_driver_id: int | None = Field(default=None, foreign_key="drivers.id")
    constructor_id: int = Field(foreign_key="teams.id")
    total_points: int = Field(default=0)
    budget_remaining: int = Field(default=100_000_000)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    __table_args__ = (
        UniqueConstraint('user_id', 'league_id', name='unique_user_league_team'),
    )
