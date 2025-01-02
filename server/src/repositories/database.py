from abc import ABC
from dataclasses import dataclass
from typing import Iterable, Any

from sqlalchemy import Executable
from src.models.base import async_session_maker, Base


@dataclass
class BaseDatabaseRepository(ABC):
    ...


@dataclass
class DatabaseRepositories(ABC):
    ...

@dataclass
class SQLAlchemyRepository(BaseDatabaseRepository):
    @staticmethod
    async def add(obj: Base) -> None:
        async with async_session_maker() as session:
            session.add(obj)
            await session.commit()

    @staticmethod
    async def merge(obj: Base) -> None:
        async with async_session_maker() as session:
            await session.merge(obj)

    @staticmethod
    async def execute(statement: Executable) -> None:
        async with async_session_maker() as session:
            await session.execute(statement)

    @staticmethod
    async def get(table: type[Base], primary_key: Any) -> Base | None:
        async with async_session_maker() as session:
            return await session.get(table, primary_key)

    @staticmethod
    async def scalar(statement: Executable) -> Any:
        async with async_session_maker() as session:
            return await session.scalar(statement)

    @staticmethod
    async def scalars(statement: Executable) -> Iterable:
        async with async_session_maker() as session:
            return await session.scalars(statement)