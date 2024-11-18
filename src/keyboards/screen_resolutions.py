from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.emoji import *


screen_resolution_photo_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Youtube', callback_data='yt_photo')],
    [InlineKeyboardButton(text='Inst (YTShorts, TikTok)', callback_data='ig_photo')],
])

screen_resolution_video_type = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Youtube', callback_data='yt_video')],
    [InlineKeyboardButton(text='Inst (YTShorts, TikTok)', callback_data='ig_video')],
])

