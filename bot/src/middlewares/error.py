from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Awaitable, Callable, Dict, Any


class ErrorMiddleware(BaseMiddleware):
    async def __call__(
                self,
                handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                event: Message, 
                data: Dict[str, Any]) -> Any:
        try:
            result = await handler(event, data)
            print(result)
            # Если результат None, значит сообщение не было обработано
            if result is None:
                await event.answer("Кажется, я не знаю, как с этим справиться! 🤔")
        except Exception as e:
            # Если возникла ошибка, отправить сообщение в чат
            await event.answer(f"Ой, что-то пошло не так! 😬 Ошибка: {str(e)}")
        
        return result
