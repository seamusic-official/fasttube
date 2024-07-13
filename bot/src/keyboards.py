from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


fireworks = "🎆"
fire = "🔥"
dollar = "💲"
check = "✅"

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'{fireworks} Создать видео')],
    [KeyboardButton(text=f'Выложить видео'), KeyboardButton(text=f'{dollar} Канал проекта', url="https://t.me/whyspacy")]
], resize_keyboard=True,
   input_field_placeholder="Выберите нужную функцию из списка.")

project_channel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text=f'{fire} SEAMUSIC', url="https://t.me/seamusicmgmt")], 
    [InlineKeyboardButton(text=f'{check} CHECK SUBCRIBE', callback_data="start")]
])

yt_or_int = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Youtube', callback_data='yt')],
    [InlineKeyboardButton(text='Inst (YTShorts, TikTok)', callback_data='ig')],
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Your channel", url="https://t.me/whyspacy")]
])

channels = [
    {
        "url": "https://www.youtube.com/channel/UCvNYCrgaij9FvtlOmtN--EA",
        "name": "YouTube"
    }
]

async def your_channels():
    keyboard = InlineKeyboardBuilder()
    for channel in channels:
        keyboard.add(InlineKeyboardButton(text=channel["name"], url=channel["url"]))
    
    return keyboard.adjust(2).as_markup()