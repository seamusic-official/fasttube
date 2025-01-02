from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Awaitable, Callable, Dict, Any



class UserMiddleware(BaseMiddleware):
    async def __call__(
                self,
                handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                event: Message, 
                data: Dict[str, Any]) -> Any:
        try:
            result = await handler(event, data)
            await ()
        except Exception as e:
            await event.answer(f"Ой, что-то пошло не так! 😬 Ошибка: {str(e)}")
        
        return result
