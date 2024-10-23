from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User
from run import async_session_maker


async def add_user(username, email):
    async with async_session_maker() as session:
        async with session.begin():
            new_user = User(username=username, email=email)
            session.add(new_user)
        await session.commit()

async def get_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        return result.scalars().all()