"""Database connection configuration."""

from pathlib import Path
from typing import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# PostgreSQL database URL from environment variable, fallback to a default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/devpulse"
)

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    """Create all tables in the database."""
    Base.metadata.create_all(bind=engine)


def drop_tables() -> None:
    """Drop all tables in the database."""
    Base.metadata.drop_all(bind=engine)
