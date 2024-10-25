from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.emoji import *


youtube = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Выложить на ютуб (Пока что не доступно)', callback_data=''),]
])