import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel
from urllib.parse import quote_plus
from f1_api.models.f1_schemas import *
from f1_api.models.app_models import *

# Load environment variables first
load_dotenv(r'C:/Users/Marc/Documents/ITA/Grid Fans/f1_api/.env')

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

encoded_password = quote_plus(PASSWORD) if PASSWORD else ""

DATABASE_URL = f"postgresql+psycopg2://{USER}:{encoded_password}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL, poolclass=NullPool)

try:
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Failed to connect: {e}")

def create_models():
    """
    Creates DB tables
    """
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Failed to create tables: {e}")
        print("Please check your database connection and try again.")

if __name__ == "__main__":
    create_models()
