from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile

profile_router = Router()

@profile_router.message(Command("profile"))
async def profile_command(message: Message):
    caption = f"Профиль FASTTUBE пользователя @{message.from_user.username}\n\nЮтуб канал: скоро\nБаланс: скоро.\nРефералы: скоро\nРеферальная ссылка для приглашений друзей: https://t.me/fasttubesmbot?start={message.from_user.id}\nПримиум: скоро | /premium\n\nАккаунт SeaMusic: скоро | /seamusic \nВсе комманды - /help"
    photo = FSInputFile("assets/fasttube-description-picture.png")
    await message.answer_photo(photo=photo, caption=caption)