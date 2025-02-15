from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from typing import Awaitable, Callable, Dict, Any

from src.utils.crud import get_data, post_data


class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Update, data: Dict[str, Any]) -> Any:
        message = event.message
        if not message:
            return await handler(event, data)
        
        try:
            existing_user = await get_data(telegram_id=str(message.from_user.id))
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
                pass

            # users = await user_repo.get_scalars_users()
            # await message.answer(f"Список пользователей: {[user.telegram_id for user in users]}")

            return await handler(event, data)
        except Exception as e:
            await message.answer(f"Упс! Чето пошло по пизде, уже исправляем. Отправь этот момент в поддержку для ускорения процесса - @seamusicmgmtbot \nОшибка: {str(e)}")