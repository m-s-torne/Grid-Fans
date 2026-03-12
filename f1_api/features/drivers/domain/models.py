"""Drivers domain models."""
from sqlalchemy import ForeignKeyConstraint
from sqlmodel import Field, SQLModel
from datetime import datetime


class Drivers(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    driver_number: int
    full_name: str
    acronym: str
    driver_color: str
    country_code: str | None
    headshot_url: str

    # MARKET PRICING FIELDS
    purchase_count: int | None = Field(default=0)  # Veces comprado en el mercado
    sale_count: int | None = Field(default=0)  # Veces vendido en el mercado
    # base_price removed - not used, fantasy_stats.price is the dynamic market price
    current_market_value: float | None = Field(default=10000000.0)  # Precio actual dinámico
    performance_score: float | None = Field(default=50.0)  # Score de rendimiento (0-100)
    last_price_update: datetime | None = Field(default=None)  # Última actualización de precio


class DriverTeamLink(SQLModel, table=True):
    driver_id: int = Field(foreign_key="drivers.id", primary_key=True)
    team_id: int = Field(foreign_key="teams.id", primary_key=True)
    season_id: int = Field(foreign_key="seasons.year", primary_key=True)
    round_number: int = Field(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ['round_number', 'season_id'],
            ['events.round_number', 'events.season_id']
        ),
    )
