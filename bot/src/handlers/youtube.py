from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.run import global_state
from src.states import PublishVideo, Connect
from aiogram.fsm.context import FSMContext
import requests
from aiogram import types
from src.utils.file_actions import download_and_save_video
from src.utils.youtube import get_auth_url

youtube_router = Router()

@youtube_router.callback_query(lambda c: c.data == 'upload_to_youtube')
async def handle_upload_to_youtube(callback_query: types.CallbackQuery, state: FSMContext):
    await connect_command(callback_query.message, state)

@youtube_router.message(Connect.credentials)
async def connect_command(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await message.answer("При нажатии на ссылку откроется страница авторизация Google, вам нужно будет выбрать тот канал на который должны будут выкладываться видео. Если вдруг высветится страница 'Эксперты Google не проверяли это приложение', то нужно нажать 'Дополнительные настройки' и нажать 'Перейти на страницу FASTTUBE (небезопасно)' \n Почему так происходит? Мы не можем получить одобрение от гугл по проверке телеграм бота, с этим, темболее из России будут возникать большие сложности.")
    
    auth_url = get_auth_url()
    await message.answer(f"При нажатии на ссылку {auth_url} откроется страница авторизация Google, вам нужно будет выбрать тот канал на который должны будут выкладываться видео. Если вдруг высветится страница 'Эксперты Google не проверяли это приложение', то нужно нажать 'Дополнительные настройки' и нажать 'Перейти на страницу FASTTUBE (небезопасно)' \n Почему так происходит? Мы не можем получить одобрение от гугл по проверке телеграм бота, с этим, темболее из России будут возникать большие сложности.")

    global_state[chat_id] = {"credentials": auth_url}
    
    await message.answer("Поздравляю! Вы подключили свой ютуб канал, теперь можете выложить видео. /upload")
    await state.set_state(Connect.credentials)


@youtube_router.message(Command("upload"))
async def upload_command(message: Message):
    chat_id = message.chat.id
    
    if "credentials" in global_state.get(chat_id, {}): 
        credentials = global_state[chat_id]["credentials"]

        await message.answer(f"Отправьте или репостните видео сделанное этим ботом ранее.")
    else:
        await message.answer("Для начала загрузки видео, нужно подключить свой ютуб канал /connect. Если вы беспокоитесь за ваши данные и безопасность - /security")

@youtube_router.message(F.video)
async def get_video_command(message: Message, state: FSMContext):
    chat_id = message.chat.id
    
    if "credentials" in global_state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре global_state[chat_id]
        credentials = global_state[chat_id]["credentials"]
        file_id = message.video.file_id
        await message.answer("Загрузка видео началась..")
        video_path = await download_and_save_video(message, file_id)
        global_state[chat_id]["video_path"] = video_path
        await message.answer("Видео успешно загружено. Теперь придумайте оригинальное название для видео.")
        await state.set_state(PublishVideo.title)
    else:
        await message.answer("Для начала нужно подключить свой ютуб канал. For this press /connect and choose your youtube channel. Security information /security")

@youtube_router.message(PublishVideo.title, F.text)
async def get_video_title(message: Message, state: FSMContext):
    chat_id = message.chat.id
    global_state[chat_id]["video_title"] = message.text
    await message.answer(f"Название: {message.text}, теперь напишите описание.")
    await state.set_state(PublishVideo.description)

@youtube_router.message(PublishVideo.description, F.text)
async def get_video_tags(message: Message, state: FSMContext):
    chat_id = message.chat.id
    global_state[chat_id]["video_description"] = message.text
    await message.answer(f"Описание: {message.text}, теперь введите теги для видео. Пример: музыка, type beat, ken karson и т.п.", parse_mode="MarkdownV2")
    await state.set_state(PublishVideo.tags)

@youtube_router.message(PublishVideo.tags, F.text)
async def get_confirm_video(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if "credentials" in global_state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре global_state[chat_id]
        global_state[chat_id]["video_tags"] = message.text
        await message.answer(f"Окей, для подтверждения загрузки, введите комманду /publish.")
        await state.set_state(PublishVideo.confirm)

@youtube_router.message(PublishVideo.confirm, F.text)
async def get_confirm_video(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if "credentials" in global_state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре global_state[chat_id]
        await message.answer(f"Видео публикуется на ваш ютуб канал.")
        credentials = global_state[chat_id]["credentials"]
        global_state[chat_id]["video_tags"] = message.text
        video_path = global_state[chat_id]["video_path"] 
        video_title = global_state[chat_id]["video_title"] 
        video_description = global_state[chat_id]["video_description"] 
        video_tags = global_state[chat_id]["video_tags"] 
        await initialize_upload(credentials, 
                                video_path, 
                                video_title, 
                                video_description + "\n\n VIDEO MAKED AND PUBLISHED BY https://t.me/fasttubesmbot", 
                                "10", 
                                "public",
                                video_tags
                                )
        
        await state.set_state(PublishVideo.tags)
        await message.answer(f"Видео опубликовано.")

