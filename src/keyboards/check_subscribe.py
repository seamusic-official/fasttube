from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.keyboards.emoji import *


check_subscribe = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f'{fire} ##SEAMUSIC', url="https://t.me/seamusicmgmt")], 
    [InlineKeyboardButton(text=f'{fire} ##FASTTUBE', url="https://t.me/fasttubeofficial")], 
    [InlineKeyboardButton(text=f'{check} CHECK SUBCRIBE', callback_data="start")]
])