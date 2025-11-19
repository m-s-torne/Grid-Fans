"""In this module the api exposes the endpoints"""
import os
import fastf1 as ff1
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
from f1_api.routers.leagues_router import router as leagues_router
from f1_api.routers.teams_router import router as teams_router
from f1_api.routers.admin_router import router as admin_router
from f1_api.routers.users_router import router as users_router
from f1_api.routers.drivers_router import router as drivers_router
from f1_api.routers.user_teams_router import router as user_teams_router
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

# Configure CORS origins from environment variable
cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
