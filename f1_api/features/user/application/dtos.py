"""Data Transfer Objects for User feature - Request/Response schemas"""
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreateDTO(BaseModel):
    """DTO for creating a new user"""
    user_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    supabase_user_id: str


class UserResponseDTO(BaseModel):
    """DTO for user response"""
    id: int
    user_name: str
    email: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
