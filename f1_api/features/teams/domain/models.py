"""Teams domain model."""
from sqlmodel import Field, SQLModel


class Teams(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    team_name: str
    team_color: str
    team_url: str | None = None
