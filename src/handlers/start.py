from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, CallbackQuery, Message
from keyboards.check_subscribe import check_subscribe
from utils.permissions import get_channel_members, get_chat_id
from keyboards.main import main

start_router = Router()

@start_router.callback_query(F.data == "start")
async def start_callback_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Нажми на /start, если подписался")

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    chat_member_seamusicmgmt = await message.bot.get_chat_member("@seamusicmgmt", message.from_user.id)
    chat_member_fasttube = await message.bot.get_chat_member("@fasttubeofficial", message.from_user.id)

    if chat_member_seamusicmgmt.status in ["member", "administrator", "creator"] and chat_member_fasttube.status in ["member", "administrator", "creator"]:
        caption = f"Привет, {message.from_user.username}! Создано разработчиком @whyspacy как часть проекта @seamusicmgmt. Бот может создавать видео из mp3 и изображения или видео (зацикливая его на всю продолжительность аудио), а затем при желании вы можете выложить видео на ютуб НАПРЯМУЮ из этого телеграм бота.\n\n/start - перезапустить \n/profile - ваш профиль\n/create_with_photo - Создать видео из фото\n/create_with_video - Создать зацикливающееся видео\n/help - все комманды \n\nНа корм разработчику и на хостинг: 2202206254377430 (Сбер)"
        try:
            photo = FSInputFile("assets/fasttube-description-picture.png")
        except Exception as e:
            print(e)
        await message.answer_photo(photo=photo, caption=caption, reply_markup=main)
    else:
        await message.answer("Для начала работы бота, нужно подписаться на создателя и канал проекта (там есть еще сервисы для артистов и продюсеров)", reply_markup=check_subscribe)
    
    # else:
        # await message.answer("Похоже, вы не учавствуете в бета тестировании. Следите за новостями в каналах @seamusicmgmt, @fasttubeofficial и @whyspacy. Если вы подавали заявку на бета тестирование, то обратитесь к @spxcyyy")

@start_router.message(F.text == "✅ Канал проекта")
async def project_channel(message: Message):
    photo = FSInputFile("assets/logofast.jpg")
    await message.answer_photo(
        photo=photo,
        caption="<b>НОВОСТИ ПРОЕКТА, ИВЕНТЫ, РОЗЫГРЫШЫ</b>\n\nКанал - https://t.me/fasttubeofficial \nДругие сервисы SeaMusic - https://t.me/seamusicmgmt",
        parse_mode="HTML"
        )

@start_router.message(F.text == "🆘 Поддержка")
async def support(message: Message):
    await message.answer(text="https://t.me/seamusicmgmtbot")

@start_router.message(F.text == "💸 На чай разработчику")
async def get_money(message: Message):
    await message.answer(text="2202206254377430 (Сбер)")