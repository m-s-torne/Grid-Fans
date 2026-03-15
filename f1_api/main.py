"""In this module the api exposes the endpoints"""
import os
import fastf1 as ff1
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from dotenv import load_dotenv
from f1_api.features.leagues.presentation.routes import router as leagues_router
from f1_api.features.teams.presentation.routes import router as teams_router
from f1_api.features.admin.presentation.routes import router as admin_router
from f1_api.features.user.presentation.routes import router as users_router
from f1_api.features.drivers.presentation.routes import router as drivers_router
from f1_api.features.user_teams.presentation.routes import router as user_teams_router
from f1_api.features.market.presentation.routes import router as market_router
# Configure FastF1 cache from environment variable
load_dotenv()
ff1_cache_dir = os.getenv('FF1_CACHE_DIR', './ff1_cache')
ff1.Cache.enable_cache(ff1_cache_dir)

app = FastAPI()

app.include_router(leagues_router, prefix="/api", tags=["Leagues"])
app.include_router(teams_router, prefix="/api", tags=["Teams"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(drivers_router, prefix="/api", tags=["Drivers"])
app.include_router(user_teams_router, prefix="/api", tags=["User Teams"])
app.include_router(market_router, prefix="/api", tags=["Market"])

# Security headers middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Configure CORS origins from environment variable
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# TrustedHostMiddleware — prevents HTTP Host header injection
allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# GZipMiddleware — compresses responses above 1 KB
app.add_middleware(GZipMiddleware, minimum_size=1000)
