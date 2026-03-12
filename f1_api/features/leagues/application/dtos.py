"""Data Transfer Objects for League feature"""
from pydantic import BaseModel, Field
from datetime import datetime


class LeagueCreateDTO(BaseModel):
    """DTO for creating a new league"""
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=200)


class LeagueResponseDTO(BaseModel):
    """DTO for league response"""
    id: int
    name: str
    description: str | None
    admin_user_id: int
    is_active: bool
    join_code: str
    current_participants: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class LeagueJoinDTO(BaseModel):
    """DTO for joining a league"""
    join_code: str = Field(..., min_length=6, max_length=10)


class LeagueListItemDTO(BaseModel):
    """DTO for league list item"""
    id: int
    name: str
    description: str | None
    is_admin: bool
    current_participants: int
    created_at: datetime
