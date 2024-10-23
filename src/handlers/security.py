from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


security_router = Router()

@security_router.message(Command("security"))
async def security_command(message: Message):
    await message.answer("If you doubt the security of connecting your account, we use oauth 2.0 (you can Google it to be absolutely sure) to authorize your Google account in our bot. this means that your personal data is not shared directly with the bot. Instead, Google's system gives the bot access to the information it needs without revealing your actual password. We only request the permissions necessary to perform the bot's functions, thereby minimizing access to your data. + you can always adjust and track all actions on your account")
