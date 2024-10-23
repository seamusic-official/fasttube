import asyncio
import logging
from aiogram.types import Message, CallbackQuery, TelegramObject, Update
from aiogram import Bot, Dispatcher, F, BaseMiddleware
from config import settings
from aiogram import types, Bot
from typing import Any, Callable, Dict, Awaitable
from middlewares.user import UserMiddleware
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine("postgresql+asyncpg://postgres:root@185.251.90.58:5432/fasttube", echo=True)
Base = declarative_base()
async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

bot = Bot(settings.telegram.TELEGRAM_API_KEY, timeout=120)
dp = Dispatcher()
global_state = {}

async def check_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    from handlers import setup 
    setup(dp)
    # await check_connection()
    # dp.message.middleware(UserMiddleware())
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")