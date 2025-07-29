"""Database connection configuration."""

from pathlib import Path
from typing import Generator
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://afaruk:158158158@localhost:5452/last_tracker_db"
)

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

# Create declarative base
Base = declarative_base()

async def get_db() -> AsyncSession:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        yield session

def create_tables() -> None:
    """Create all tables in the database."""
    import asyncio
    async def _create():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(_create())

def drop_tables() -> None:
    """Drop all tables in the database."""
    import asyncio
    async def _drop():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(_drop())
