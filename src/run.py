import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.middlewares.auth import AuthMiddleware

global_state = {}


bot = Bot("7241033278:AAG4YXnZj-jtUW4xgQUqDYDy5MVQneaArdY", timeout=120)
dp = Dispatcher()

async def main():
    from src.handlers.create_video import create_video_router  # Переместили сюда
    from src.handlers.help import help_router
    from src.handlers.newsletter import newsletter_router
    from src.handlers.profile import profile_router
    from src.handlers.security import security_router
    from src.handlers.start import start_router
    from src.handlers.youtube import youtube_router

    logging.basicConfig(level=logging.DEBUG)

    dp.include_router(create_video_router)
    dp.include_router(help_router)
    dp.include_router(newsletter_router)
    dp.include_router(profile_router)
    dp.include_router(security_router)
    dp.include_router(start_router)
    dp.include_router(youtube_router)
    
    dp.update.middleware(AuthMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())