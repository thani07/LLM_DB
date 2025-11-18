# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Please set DATABASE_URL in your environment or .env file")

# Special handling for SQL Server (only for local system)
if DATABASE_URL.startswith("mssql"):
    engine = create_engine(
        DATABASE_URL,
        fast_executemany=True,
        echo=False
    )
else:
    # This will be used by PostgreSQL on Render
    engine = create_engine(
        DATABASE_URL,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
