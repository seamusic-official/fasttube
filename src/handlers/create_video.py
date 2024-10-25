from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.types import FSInputFile
from run import global_state
from moviepy.editor import VideoFileClip
from aiogram.fsm.context import FSMContext
from states import CreateVideo, CreateVideoFromVideo
from utils.file_actions import delete_file, download_and_save_audio, download_and_save_photo, download_and_save_video
from utils.moviepy import create_instagram_video_with_centered_image, create_instagram_video_with_repeating_video, create_video_with_repeating_video, create_video_with_stretched_image
from keyboards.screen_resolutions import screen_resolution_photo_type, screen_resolution_video_type
from keyboards.menu import youtube
from keyboards.main import main


create_video_router = Router()

@create_video_router.callback_query(lambda query: query.data in ['yt_video', 'ig_video'])
async def process_callback_video_type(callback_query: CallbackQuery):
    answer = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if chat_id in global_state:
        if answer == 'yt_video':
            await create_video_from_video_for_youtube(callback_query.message)
        elif answer == 'ig_video':
            await create_video_from_video_for_instagram(callback_query.message)

@create_video_router.callback_query(lambda query: query.data in ['yt_photo', 'ig_photo'])
async def process_callback_photo_type(callback_query: CallbackQuery):
    answer = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if chat_id in global_state:
        if answer == 'yt_photo':
            await create_video_for_youtube(callback_query.message)
        elif answer == 'ig_photo':
            await create_video_for_instagram(callback_query.message)


@create_video_router.message(F.text == "🎆 Создать видео из фото")
@create_video_router.message(Command("create_with_photo"))
async def create_video(message: Message, state: FSMContext):
    photo = FSInputFile("assets/photovideo.jpg")
    await message.answer_photo(photo=photo,
                               caption="Для начала процесса создания видео из фотографии, скиньте качественное изображение для того вида видео, которое хотите получить. Затем вы сможете скинуть mp3 и выбрать разрешение (YouTube, Instagram)",
                               reply_markup=main)

    await state.set_state(CreateVideo.image)

@create_video_router.message(CreateVideo.image, F.photo)
async def get_photo(message: Message):
    chat_id = message.chat.id
    if chat_id not in global_state:
        global_state[chat_id] = {}  # Инициализируем глобальное состояние для chat_id, если его нет

    try:
        file_id = message.photo[-1].file_id
        global_state[chat_id]["photo_id"] = await download_and_save_photo(message, file_id)
        await message.answer("Изображение успешно загружено! Теперь скиньте аудиофайл исключительно формата mp3.")
    
    except Exception as e:
        await message.answer(f"Произошла ошибка: {str(e)}. Пожалуйста, попробуйте еще раз.")


@create_video_router.message(CreateVideo.image, F.audio)
async def get_audio(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        try:
            photo_path = global_state[chat_id]["photo_id"]
            audio_file_id = message.audio.file_id
            audio_path = await download_and_save_audio(message, audio_file_id)
            global_state[chat_id] = {"photo_path": photo_path, "audio_path": audio_path}
            await message.answer("Выберите формат видео: ", reply_markup=screen_resolution_photo_type)
        
        except Exception as e:
            await message.answer(f"Произошла ошибка: {str(e)}. Попробуйте еще раз, пожалуйста!")
    else:
        await message.answer("Для создания видео загрузи сначала изображение, а затем аудиофайл.", reply_markup=main)

@create_video_router.message(F.text == "🎆 Зациклить видео по длине mp3")
@create_video_router.message(Command("create_with_video"))
async def create_video_from_video(message: Message, state: FSMContext):
    await message.answer("Для начала процесса создания зацикливающегося видео по длине mp3, скиньте качественное видео для того вида видео, которое хотите получить. Затем вы сможете скинуть mp3 и выбрать разрешение (YouTube, Instagram)")
    await state.set_state(CreateVideoFromVideo.video)

@create_video_router.message(CreateVideoFromVideo.video, F.video)
async def get_video_for_video_from_video(message: Message):
    
    chat_id = message.chat.id
    if chat_id not in global_state:
        global_state[chat_id] = {}

    file_id = message.video.file_id
    global_state[chat_id]["video_id"] = await download_and_save_video(message, file_id)
    await message.answer("Видео файл успешно загружен! Теперь скиньте аудиофайл исключительно формата mp3.")


@create_video_router.message(CreateVideoFromVideo.video, F.audio)
async def get_audio_for_video_from_video(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        video_path = global_state[chat_id]["video_id"]
        audio_file_id = message.audio.file_id
        audio_path = await download_and_save_audio(message, audio_file_id)
        global_state[chat_id] = {"video_path": video_path, "audio_path": audio_path}
        await message.answer("Выберите формат видео: ", reply_markup=screen_resolution_video_type)
    else:
        await message.answer("Для создания видео загрузи видео файл, а затем аудиофайл.")

async def create_video_from_video_for_youtube(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для ютубе! Обычно процесс занимает 1-2 минуты")

        video_path = global_state[chat_id]["video_path"]
        audio_path = global_state[chat_id]["audio_path"]

        video_data = await create_video_with_repeating_video(audio_path, video_path)

        await message.answer("Успешно!", reply_markup=youtube)

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input, reply_markup=main)

async def create_video_for_youtube(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        try:
            await message.answer("Началось создание видео для ютуба! Обычно процесс занимает 1-2 минуты")

            photo_path = global_state[chat_id]["photo_path"]
            audio_path = global_state[chat_id]["audio_path"]

            video_data = await create_video_with_stretched_image(audio_path, photo_path)

            await message.answer("Успешно!")

            video_input = FSInputFile(video_data["video_path"])
            await message.answer_video(video_input, reply_markup=main)
            await message.answer("Теперь вы можете загрузить его на ютуб. (функция выгрузки через бота появится через некоторое время, следите за новостями - @fasttubeofficial)", reply_markup=youtube)
            
            await delete_file(video_data["video_path"])
            await delete_file(photo_path)
            await delete_file(audio_path)
        except Exception as e:
            await message.answer(f"Ой! Произошла ошибка при создании видео для ютуба: {str(e)}. Пожалуйста, попробуй еще раз.")

async def create_video_for_instagram(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        try:
            await message.answer("Началось создание видео для инстаграма! Обычно процесс занимает 1-2 минуты")

            photo_path = global_state[chat_id]["photo_path"]
            audio_path = global_state[chat_id]["audio_path"]

            video_data = await create_instagram_video_with_centered_image(audio_path, photo_path)

            await message.answer("Успешно!")

            video_input = FSInputFile(video_data["video_path"])
            await message.answer_video(video_input)
            await message.answer("Теперь вы можете загрузить его на поддерживающие вертикальный формат видео площадки. (функция выгрузки через бота появится через некоторое время, следите за новостями - @fasttubeofficial)")
            
            await delete_file(video_data["video_path"])
            await delete_file(photo_path)
            await delete_file(audio_path)
        except Exception as e:
            await message.answer(f"Ой! Произошла ошибка при создании видео для инстаграма: {str(e)}. Пожалуйста, попробуй еще раз.")

async def create_video_from_video_for_instagram(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для инстраграма! Обычно процесс занимает 1-2 минуты")

        try:
            video_path = global_state[chat_id]["video_path"]
            audio_path = global_state[chat_id]["audio_path"]

            video_data = await create_instagram_video_with_repeating_video(audio_path, video_path)

            await message.answer("Успешно!")

            video_input = FSInputFile(video_data["video_path"])
            await message.answer_video(video_input, youtube)
            await message.answer("Теперь вы можете загрузить его на поддерживающие вертикальный формат видео площадки. (функция выгрузки через бота появится через некоторое время, следите за новостями - @fasttubeofficial)", reply_markup=main)

            await delete_file(video_data["video_path"])
            await delete_file(video_path)
            await delete_file(audio_path)

        except Exception as e:
            await message.answer(f"Произошла ошибка при создании видео: {str(e)}. Пожалуйста, попробуйте еще раз!")
    else:
        await message.answer("Сначала загрузите видео и аудиофайл, чтобы создать видео!")
