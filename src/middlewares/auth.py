from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from typing import Awaitable, Callable, Dict, Any
from src.repositories.auth import UserRepository
import logging

logging.basicConfig(level=logging.ERROR)
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.CRITICAL)
logging.basicConfig(level=logging.INFO)


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Update, data: Dict[str, Any]) -> Any:
        message = event.message
        if not message:
            return await handler(event, data)

        user_repo = UserRepository()  # Проверь, как ты инициализируешь этот репозиторий
        
        try:
            existing_user = await user_repo.get_users_with_filters(telegram_id=str(message.from_user.id))
            print("Существующий пользователь:", existing_user)

            if existing_user is None or next(existing_user, None) is None:
                response = await user_repo.add_user(
                    username=message.from_user.username or f"ftuser-{message.from_user.id}",
                    full_name=message.from_user.full_name,
                    telegram_id=str(message.from_user.id)
                )
                print("Регистрация:", response)
                await message.answer("Поздравляем с регистрацией! 🎉")
            else:
                await message.answer("С возвращением! 👋")

            users = await user_repo.get_scalars_users()
            await message.answer(f"Список пользователей: {[user.telegram_id for user in users]}")

            return await handler(event, data)
        except Exception as e:
            logging.error("Ошибка: %s", str(e), exc_info=True)
            await message.answer(f"Упс! Чето пошло не так. Отправь это в поддержку - @seamusicmgmtbot \nОшибка: {str(e)}")