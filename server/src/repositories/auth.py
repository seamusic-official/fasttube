from typing import Optional
from sqlalchemy import Executable, func, select, delete
from src.repositories.database import SQLAlchemyRepository
from src.models import User
from typing import Iterable
from dataclasses import dataclass

@dataclass
class UserRepository(SQLAlchemyRepository):
    @staticmethod
    async def add_user(username: str, full_name: str, telegram_id: str) -> User:
        new_user = User(username=username, full_name=full_name, telegram_id=telegram_id)
        await SQLAlchemyRepository.add(new_user)
        return new_user

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        return await SQLAlchemyRepository.get(User, user_id)

    @staticmethod
    async def get_users_with_filters(**kwargs) -> Iterable[User]:
        statement = select(User)
        
        if kwargs:
            filters = [getattr(User, key) == value for key, value in kwargs.items()]
            statement = statement.where(*filters)
        
        return await SQLAlchemyRepository.scalars(statement)
    
    @staticmethod
    async def get_scalars_users():
        query: Executable = select(User)
        models: Iterable[User] = await SQLAlchemyRepository.scalars(query)
        return list(models)

    @staticmethod
    async def update_user(user_id: int, username: Optional[str] = None, full_name: Optional[str] = None, telegram_id: Optional[str] = None) -> Optional[User]:
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            if username is not None:
                user.username = username
            if full_name is not None:
                user.full_name = full_name
            if telegram_id is not None:
                user.telegram_id = telegram_id
            await SQLAlchemyRepository.merge(user)
            return user
        return None

    @staticmethod
    async def delete_user(user_id: int) -> None:
        user = await UserRepository.get_user_by_id(user_id)
        if user:
            await SQLAlchemyRepository.execute(User.table.delete().where(User.id == user_id))