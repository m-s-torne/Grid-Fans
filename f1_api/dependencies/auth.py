"""Authentication dependency — Supabase JWT verification"""
import os
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlmodel import Session, select
from f1_api.dependencies.database import get_db_session
from f1_api.features.user.domain.models import Users

bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: Session = Depends(get_db_session),
) -> Users:
    secret = os.getenv("SUPABASE_JWT_SECRET")
    if not secret:
        raise HTTPException(status_code=500, detail="Auth not configured")
    try:
        payload = jwt.decode(credentials.credentials, secret, algorithms=["HS256"],
                             options={"verify_aud": False})
        supabase_user_id = payload.get("sub")
        if not isinstance(supabase_user_id, str):
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc

    user = session.exec(select(Users).where(Users.supabase_user_id == supabase_user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_admin_user(current_user: Users = Depends(get_current_user)) -> Users:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
