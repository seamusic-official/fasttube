from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.states import CreateNew
from aiogram.fsm.context import FSMContext
import requests

newsletter_router = Router()

async def send_newsletter(message: Message, id_users):
    for telegram_id in id_users:
        await message.bot.send_photo(telegram_id, photo=message.photo[-1].file_id, caption=message.caption)

@newsletter_router.message(Command("new"))
async def forward_message(message: Message, state: FSMContext):
    if message.from_user.username == "spxcyyy":
        await message.answer("Теперь отправляй новость")
        await state.set_state(CreateNew.is_continue)

@newsletter_router.message(CreateNew.is_continue, F.photo)
async def forward_message_state(message: Message):  
    if message.from_user.username == "spxcyyy":
        users = await user_repo.get_scalars_users()
        id_users = [user.telegram_id for user in users]
        await send_newsletter(message, id_users)
