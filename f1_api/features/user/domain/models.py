from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField


class Users(SQLModel, table=True):
    id: int = SQLField(default=None, primary_key=True)
    user_name: str = SQLField(unique=True, index=True)
    email: str = SQLField(unique=True, index=True)
    supabase_user_id: str = SQLField(unique=True, index=True)
    is_verified: bool = SQLField(default=False)
    is_admin: bool = SQLField(default=False)
    created_at: datetime = SQLField(default_factory=datetime.now)


class UserCreate(BaseModel):
    user_name: str
    email: str
    supabase_user_id: str


class UserResponse(BaseModel):
    id: int
    user_name: str
    email: str
    is_verified: bool
    created_at: datetime
