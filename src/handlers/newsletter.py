from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from handlers.crud.crud import get_users
from states import CreateNew
from aiogram.fsm.context import FSMContext
import requests

newsletter_router = Router()

async def send_newsletter(message: Message, all_users):
    for user_id in all_users:
        await message.bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)

@newsletter_router.message(Command("new"))
async def forward_message(message: Message, state: FSMContext):
    if message.from_user.username == "spxcyyy":
        await message.answer("Теперь отправляй новость")
        await state.set_state(CreateNew.is_continue)

@newsletter_router.message(CreateNew.is_continue, F.photo)
async def forward_message_state(message: Message):  
    if message.from_user.username == "spxcyyy":
        all_users = await get_users()
        id_users = []

        for id in all_users:
            id_users.append(id)

        await send_newsletter(message, all_users)
