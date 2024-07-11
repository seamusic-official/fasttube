from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from src.keyboards import your_channels, project_channel
import numpy as np
from src.utils import create_video_with_stretched_image, authenticate, upload_video
import os
import uuid
from aiogram.types import FSInputFile, CallbackQuery

router = Router()
state = {}
from aiogram import types

@router.callback_query(F.data == "start")
async def start_callback_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Press /start, if you're subscribed")

@router.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = "@seamusicmgmt"
    chat_member = await message.bot.get_chat_member(chat_id, message.from_user.id)
            
    if chat_member.status in ["member", "administrator", "creator"]:
        await message.answer(f"Wassup, {message.from_user.username}! This is a bot created by @whyspacy, which can help to publish your videos to YouTube without a browser.\n\n/start - RESTART \n/profile - PROFILE\n/help - ALL COMMANDS \n")    
    else:
        await message.answer("For the bot to work, you need to subscribe to project channel", reply_markup=project_channel)

        
@router.message(Command("help"))
async def cmd_message(message: Message):
    await message.answer("\n/start - RESTART \n/help - ALL COMMANDS \n/create - CREATE VIDEO WITH IMAGE \n/connect - CONNECT YOUTUBE CHANNEL /security - WHY IS IT SAFE \n/upload - UPLOAD VIDEO \n/seamusic - SEAMUSIC ACCOUNT | ? \n/profile - FASTTUBE PROFILE")

@router.message(F.photo)
async def get_photo(message: Message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id
    state[chat_id] = {"photo_id": await download_and_save_photo(message, file_id)}
    await message.answer("Изображение успешно загружено! Теперь скиньте аудиофайл исключительно формата mp3.")

async def download_and_save_photo(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    photo_path = f"temp_photo_{os.path.basename(file_path)}"
    with open(photo_path, "wb") as photo_file:
        photo_file.write(downloaded_file.read())
    return photo_path

@router.message(F.audio)
async def get_audio(message: Message):
    chat_id = message.chat.id
    if chat_id in state:
        photo_path = state[chat_id]["photo_id"]
        audio_file_id = message.audio.file_id
        audio_path = await download_and_save_audio(message, audio_file_id)
        
        await message.answer("Началось создание видео! Обычно процесс занимает 1-2 минуты")

        video_data = await create_video_with_stretched_image(audio_path, photo_path)
        state[chat_id] = {"video_path": video_data["video_path"]} 
        state[chat_id] = {"photo_path": photo_path, "audio_path": audio_path}
        video_id = str(uuid.uuid4())
        thumbnail_id = str(uuid.uuid4())

        await message.answer("Успешно!")

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input)
        await message.answer("Теперь вы можете загрузить его на ютуб по команде /upload")
    else:
        await message.answer("Для создания видео загрузи сначала изображение, а затем аудиофайл.")

async def download_and_save_audio(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    audio_path = f"temp_audio_{os.path.basename(file_path)}"
    with open(audio_path, "wb") as audio_file:
        audio_file.write(downloaded_file.read())
    return audio_path

import asyncio

@router.message(Command("connect"))
async def connect_command(message: Message):

    chat_id = message.chat.id
    credentials = await authenticate()
    state[chat_id] = {"credentials": credentials}
    
    await message.answer("You're connected your channel, now you can to upload video in youtube channel /upload")


@router.message(Command("upload"))
async def upload_command(message: Message):
    chat_id = message.chat.id
    
    if "credentials" in state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре state[chat_id]
        credentials = state[chat_id]["credentials"]
        
        await message.answer(f"Send or repost created on fasttube video here, after we can to change tags for video and upload it on YT")
    else:
        await message.answer("For starting need to connect your channel. For this press /connect and choose your youtube channel. Security information /security")

@router.message(F.video)
async def get_video_command(message: Message):
    chat_id = message.chat.id
    
    if "credentials" in state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре state[chat_id]
        credentials = state[chat_id]["credentials"]
        file_id = message.video.file_id
        video_path = await download_and_save_video(message, file_id)
        video_data = {
            "title": "title",
            "description": "description",
            "video_path": video_path
        }
        asyncio.create_task(upload_video(video_data=video_data, credentials=credentials))
    else:
        await message.answer("For starting need to connect your channel. For this press /connect and choose your youtube channel. Security information /security")

async def download_and_save_video(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    video_path = f"any_video_{os.path.basename(file_path)}"
    with open(video_path, "wb") as video_file:
        video_file.write(downloaded_file.read())
    return video_path

@router.message(Command("security"))
async def security_command(message: Message):
    await message.answer("If you doubt the security of connecting your account, we use oauth 2.0 (you can Google it to be absolutely sure) to authorize your Google account in our bot. this means that your personal data is not shared directly with the bot. Instead, Google's system gives the bot access to the information it needs without revealing your actual password. We only request the permissions necessary to perform the bot's functions, thereby minimizing access to your data. + you can always adjust and track all actions on your account")

@router.message(Command("create"))
async def create_video_command(message: Message):
    await message.answer("For creating video, send good quality image in chat.")

@router.message(Command("profile"))
async def profile_command(message: Message):
    caption = f"| FASTTUBE PROFILE FOR @{message.from_user.username} |\n\nYOUTUBE ACCOUNT: TRUE | /connect\nBALANCE: 8234р.\nFRIENDS: 23\nREFERRAL LINK: https://\nPREMIUM: TRUE | /premium\n\nSEAMUSIC ACCOUNT: TRUE | /seamusic \nFOR HELP - /help"
    photo = FSInputFile("fasttube.jpg")
    await message.answer_photo(photo=photo, caption=caption)

@router.message(Command("create"))
async def create_video_command(message: Message):
    await message.answer("For creating video, send good quality image in chat.")
