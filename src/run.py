import asyncio
import logging
from aiogram import Bot, Dispatcher
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_async_engine("postgresql+asyncpg://postgres:root@185.251.90.58:5432/fasttube", echo=True)
Base = declarative_base()
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

bot = Bot("7241033278:AAG4YXnZj-jtUW4xgQUqDYDy5MVQneaArdY", timeout=120)
dp = Dispatcher()
global_state = {}

async def check_connection():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    from handlers import setup
    setup(dp)
    
    # await check_connection()  # Если это нужно, раскомментируй
    # dp.message.middleware(UserMiddleware())  # Если нужно использовать middleware

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    while True:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.error(f"Бот потерпел неисправность: {e}")
            asyncio.sleep(5)  # Подождем перед перезапуском
