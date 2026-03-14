# Security – Middleware & Auth Guards

## Context

Stack: Python 3.12, FastAPI, SQLModel, Supabase (JWT auth). Workspace root: `c:\Users\Marc\Documents\ITA\Grid Fans`. `.venv` is at `f1_api/.venv`. All imports use the `f1_api.` prefix.

Auth model: users have a `supabase_user_id: str` column. Supabase issues JWTs signed with a secret (`SUPABASE_JWT_SECRET` env var). No route currently verifies any token — all routes are fully open.

Philosophy reminder:
- **Middleware** = HTTP-layer, context-free, uniform rules (headers, compression, host validation)
- **`Depends()`** = application-layer, context-aware, resource-specific rules (auth, authorization)

---

## Part 1 — HTTP-layer middleware (add to `main.py`)

### 1a — Delete dead code

Delete `f1_api/middleware/error_handling.py`. It is never registered and cannot function correctly (it has no access to the DB session needed for `session.rollback()`).

### 1b — TrustedHostMiddleware

Prevents HTTP Host header injection attacks.

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)
```

Add `ALLOWED_HOSTS` to `.env` with production domain when deploying.

### 1c — GZipMiddleware

Compresses JSON responses above 1 KB. Free performance win for list endpoints.

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### 1d — Security headers middleware

Adds OWASP-recommended response headers. Implement as a custom `@app.middleware("http")` in `main.py` (not a separate file — it is two lines of business logic, not worth its own module):

```python
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response
```

Add `from fastapi import Request` to `main.py` imports.

### 1e — Tighten CORS config

Current config uses `allow_methods=["*"]` and `allow_headers=["*"]`. Scope these down:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## Part 2 — Authentication dependency (`Depends()`)

### 2a — Create `f1_api/dependencies/auth.py`

This module provides a reusable `get_current_user` dependency that:
1. Extracts the Bearer token from the `Authorization` header
2. Verifies the JWT signature using `SUPABASE_JWT_SECRET`
3. Extracts `sub` claim (= `supabase_user_id`)
4. Looks up the matching `Users` row in the DB
5. Returns the `Users` object, or raises `401`

Required package: `python-jose[cryptography]`. Add to `f1_api/requirements.txt`.

```python
"""Authentication dependency — Supabase JWT verification"""
import os
from fastapi import Depends, HTTPException, status
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
        supabase_user_id: str = payload.get("sub")
        if not supabase_user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = session.exec(select(Users).where(Users.supabase_user_id == supabase_user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

Export from `f1_api/dependencies/__init__.py`.

### 2b — Apply `get_current_user` to all protected routers

Add as a router-level dependency so every route in the router is protected without touching individual route functions:

```python
# In each presentation/routes.py that requires auth:
from f1_api.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/leagues",
    tags=["leagues"],
    dependencies=[Depends(get_current_user)],
)
```

Apply to: `leagues`, `user_teams`, `market`, `teams`, `drivers` routers.

**Leave `users` router open** — the `POST /users/` registration endpoint must be accessible before the user exists in DB.

**Leave `admin` router for Part 3.**

### 2c — Remove `user_id` query parameters from protected routes

Several routes currently accept `user_id: str` as an open query parameter (e.g. `GET /users/my-teams?user_id=...`). Once auth is in place, replace these with the injected `current_user`:

```python
# Before:
def get_my_teams(user_id: str, session: Session = Depends(get_db_session)):

# After:
def get_my_teams(
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
):
    # use current_user.supabase_user_id instead of user_id param
```

This closes the broken access control vulnerability (OWASP A01) where any user can request any other user's data by supplying their ID.

---

## Part 3 — Admin authorization guard

The `admin` router controls data ingestion. It must be restricted to admin users only.

### 3a — Add `is_admin` flag to `Users` model

```python
class Users(SQLModel, table=True):
    ...
    is_admin: bool = SQLField(default=False)
```

Create a DB migration (Alembic or raw SQL `ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT FALSE`).

### 3b — Create `get_admin_user` dependency in `f1_api/dependencies/auth.py`

```python
def get_admin_user(current_user: Users = Depends(get_current_user)) -> Users:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

### 3c — Apply to admin router

```python
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_admin_user)],
)
```

---

## Part 4 — League membership authorization

Beyond authentication (who are you?), market and team routes need authorization (are you a member of *this* league?).

Create a reusable dependency:

```python
# f1_api/features/leagues/dependencies.py
def get_league_member(
    league_id: int,
    session: Session = Depends(get_db_session),
    current_user: Users = Depends(get_current_user),
) -> Users:
    """Raises 403 if current_user is not a member of league_id"""
    membership = session.exec(
        select(LeagueMember)
        .where(LeagueMember.league_id == league_id)
        .where(LeagueMember.user_id == current_user.id)
    ).first()
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this league")
    return current_user
```

Apply at the route level (not router level, since it needs `league_id` from the path):

```python
@router.post("/{league_id}/market/buy/{driver_id}")
def buy_driver(
    league_id: int,
    driver_id: int,
    current_user: Users = Depends(get_league_member),  # verifies membership
    session: Session = Depends(get_db_session),
):
```

---

## Implementation order

1. Part 1 (middleware) — no breaking changes, safe to do immediately
2. Part 2a–2b (JWT dependency + router guards) — coordinate with frontend to send `Authorization: Bearer <token>` header
3. Part 2c (remove `user_id` query params) — update frontend calls simultaneously
4. Part 3 (admin guard + DB migration) — requires DB migration, do in a controlled deploy
5. Part 4 (league membership) — final hardening pass

---

## Files to create / modify

| Action | File |
|---|---|
| DELETE | `f1_api/middleware/error_handling.py` |
| MODIFY | `f1_api/main.py` |
| CREATE | `f1_api/dependencies/auth.py` |
| MODIFY | `f1_api/dependencies/__init__.py` |
| MODIFY | `f1_api/features/user/domain/models.py` (add `is_admin`) |
| MODIFY | `f1_api/features/leagues/presentation/routes.py` |
| MODIFY | `f1_api/features/leagues/presentation/market_routes.py` |
| MODIFY | `f1_api/features/leagues/presentation/team_routes.py` |
| MODIFY | `f1_api/features/user_teams/presentation/routes.py` |
| MODIFY | `f1_api/features/market/presentation/routes.py` |
| MODIFY | `f1_api/features/teams/presentation/routes.py` |
| MODIFY | `f1_api/features/drivers/presentation/routes.py` |
| MODIFY | `f1_api/features/admin/presentation/routes.py` |
| CREATE | `f1_api/features/leagues/dependencies.py` |
| ADD TO | `f1_api/requirements.txt` (`python-jose[cryptography]`) |
