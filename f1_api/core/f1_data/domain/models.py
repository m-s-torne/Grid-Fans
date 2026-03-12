"""Core F1 data domain models — seasons, events, sessions, results."""
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, DateTime, String
from sqlmodel import Field, SQLModel
from datetime import datetime


class Seasons(SQLModel, table=True):
    year: int = Field(primary_key=True)


class Events(SQLModel, table=True):
    round_number: int = Field(default=None, primary_key=True)
    season_id: int = Field(default=None, foreign_key="seasons.year", primary_key=True)
    event_name: str
    event_type: str
    event_country: str
    date_start: datetime = Field(sa_column=Column(DateTime))

    __table_args__ = (
        UniqueConstraint('season_id', 'event_name'),
    )


class Sessions(SQLModel, table=True):
    round_number: int = Field(primary_key=True)
    season_id: int = Field(primary_key=True)
    session_number: int = Field(primary_key=True)
    session_type: str | None

    __table_args__ = (
        ForeignKeyConstraint(
            ['round_number', 'season_id'],
            ['events.round_number', 'events.season_id']
        ),
    )


class SessionResult(SQLModel, table=True):
    season_id: int | None = Field(default=None, primary_key=True)
    round_number: int = Field(primary_key=True)
    session_number: int = Field(primary_key=True)
    driver_id: int = Field(foreign_key="drivers.id", primary_key=True)
    position: str | None = Field(default=None, sa_column=Column(String(10)))
    grid_position: int | None
    best_lap_time: float | None
    total_time: float | None
    points: int | None
    status: str | None
    fastest_lap: bool | None

    __table_args__ = (
        ForeignKeyConstraint(
            ['round_number', 'season_id', 'session_number'],
            ['sessions.round_number', 'sessions.season_id', 'sessions.session_number']
        ),
    )
