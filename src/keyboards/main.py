from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.emoji import *


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'{fireworks} Создать видео')],
    [KeyboardButton(text=f'Выложить видео'), KeyboardButton(text=f'{dollar} Канал проекта', url="https://t.me/whyspacy")]
], resize_keyboard=True,
   input_field_placeholder="Выберите нужную функцию из списка.")

