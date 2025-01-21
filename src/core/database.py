from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings

__all__ = (
    "Base",
    "Session",
    "AsyncSession",
    "get_async_session",
    "init_db",
)


# POSTGRES_INDEXES_NAMING_CONVENTION = {
#     "ix": "%(column_0_label)s_idx",
#     "uq": "%(table_name)s_%(column_0_name)s_key",
#     "ck": "%(table_name)s_%(constraint_name)s_check",
#     "fk": "%(table_name)s_%(column_0_name)s_fkey",
#     "pk": "%(table_name)s_pkey",
# }

POSTGRES_INDEXES_NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s_%(column_0_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "ix": "ix_%(column_0_label)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
}

metadata = MetaData(naming_convention=POSTGRES_INDEXES_NAMING_CONVENTION)


class Base(AsyncAttrs, DeclarativeBase):
    metadata = metadata

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"


asyncio_engine = create_async_engine(
    settings.db.dsn,
    echo=settings.debug,
)

AsyncSessionFactory = async_sessionmaker(
    asyncio_engine,
    autocommit=False,
    expire_on_commit=False,
    future=True,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {asyncio_engine.pool.status()}")
        yield session


async def init_db():
    async with asyncio_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


Session = Annotated[AsyncSession, Depends(get_async_session)]
