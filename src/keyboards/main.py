from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.emoji import *


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=f'{fireworks} Создать видео из фото'), KeyboardButton(text=f'{fireworks} Зациклить видео по длине mp3')],
    [KeyboardButton(text=f'{money} На чай разработчику'), KeyboardButton(text=f'{sos} Поддержка', url="https://t.me/seamusicmgmtbot")],
    [KeyboardButton(text=f'{check} Канал проекта', url="https://t.me/fasttubeofficial")],
], resize_keyboard=True,
   input_field_placeholder="Выберите нужную функцию из списка.")

