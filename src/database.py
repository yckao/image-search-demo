# pylint: disable=too-few-public-methods
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src import config


class Base(DeclarativeBase): ...


engine = create_async_engine(
    config.settings.postgres_url,
    echo=config.settings.environment == "development",
)  # type: ignore  # Async database engine instance for PostgreSQL

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)  # Async session factory for database operations
