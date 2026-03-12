"""User Teams application DTOs - Data Transfer Objects"""
from pydantic import BaseModel, Field
from datetime import datetime


class UserTeamCreateDTO(BaseModel):
    """DTO for creating a basic user team"""
    user_id: int
    league_id: int
    team_name: str
    driver_1_id: int
    driver_2_id: int
    driver_3_id: int
    reserve_driver_id: int | None = None
    constructor_id: int
    budget_remaining: int


class UserTeamUpdateDTO(BaseModel):
    """DTO for updating a user team"""
    team_name: str = Field(min_length=4, max_length=50)
    driver_1_id: int
    driver_2_id: int
    driver_3_id: int
    constructor_id: int
    budget_remaining: int | None = None


class SwapReserveDriverDTO(BaseModel):
    """DTO for swapping reserve driver request"""
    user_id: int = Field(..., description="Internal user ID (not Supabase ID)")
    driver_id: int = Field(..., description="Driver to make reserve (will swap with current reserve)")


class UserTeamResponseDTO(BaseModel):
    """DTO for user team response"""
    id: int
    user_id: int
    league_id: int
    team_name: str
    driver_1_id: int
    driver_2_id: int
    driver_3_id: int
    reserve_driver_id: int | None
    constructor_id: int
    total_points: int
    budget_remaining: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
