from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

help_router = Router()

@help_router.message(Command("help"))
async def cmd_message(message: Message):
    await message.answer(
        "\n/start - Перезапустить \n/create_with_photo - Создать видео из фото\n/create_with_video - Создать зацикливающееся видео\n/seamusic - Аккаунт SEAMUSIC | <a href='https://t.me/seamusicmgmt'>(?)</a>\n/profile - Ваш профиль",
        parse_mode='HTML'
    )