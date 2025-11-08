"""In this module the api exposes the endpoints"""
import fastf1 as ff1
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
#from f1_api.controllers.routes import router as legacy_router
from f1_api.routers.leagues_router import router as leagues_router
from f1_api.routers.teams_router import router as teams_router
from f1_api.routers.admin_router import router as admin_router
from f1_api.routers.users_router import router as users_router
from f1_api.routers.drivers_router import router as drivers_router
from f1_api.routers.user_teams_router import router as user_teams_router

ff1.Cache.enable_cache(r'C:/Users/Marc/Documents/ITA/Grid Fans/f1_api/ff1_cache')

app = FastAPI()

app.include_router(leagues_router, prefix="/api", tags=["Leagues"])
app.include_router(teams_router, prefix="/api", tags=["Teams"])
app.include_router(admin_router, prefix="/api", tags=["Admin"])
app.include_router(users_router, prefix="/api", tags=["Users"])
app.include_router(drivers_router, prefix="/api", tags=["Drivers"])
app.include_router(user_teams_router, prefix="/api", tags=["User Teams"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
