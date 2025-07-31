import logging

from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from src.base_settings import base_settings


logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self):
        self.__session = None
        self._engine = None

    def connect(self, db_config):
        self._engine = create_async_engine(
            url=base_settings.postgres.url,
        )

        self.__session = async_sessionmaker(
            bind=self._engine,
            autocommit=False,
        )

    async def disconnect(self):
        await self._engine.dispose()

    def get_engine(self):
        return self._engine

    async def get_db(self):
        async with postgres.__session() as session:
            yield session


postgres = Database()


async def get_session():
    async for session in postgres.get_db():
        yield session