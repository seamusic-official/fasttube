from aiogram import BaseMiddleware
from aiogram.types import Message, Update
from typing import Awaitable, Callable, Dict, Any
from repositories.auth import UserRepository

class AuthMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Update, data: Dict[str, Any]) -> Any:
        # We're assuming 'event' is your 'Update' object, so let's get the message from it
        message = event.message
        if not message:
            return await handler(event, data)  # If there's no message, just proceed as normal.

        try:
            # Log the user into the repository
            await UserRepository.add_user(
                username=message.from_user.username if message.from_user.username else f"ftuser-{message.from_user.id}",
                full_name=message.from_user.full_name,
                telegram_id=message.from_user.id
            )
            users = await UserRepository.get_all_users()
            await message.answer(users)

            return await handler(event, data)
        except Exception as e:
            await message.answer(f"Oops! Something went wrong! 😬 Error: {str(e)}")