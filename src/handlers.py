from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InputFile
from aiogram.types import FSInputFile, CallbackQuery
from src.keyboards import your_channels, project_channel, yt_or_inst_for_photo_type, yt_or_inst_for_video_type
from src.utils import create_video_with_stretched_image, create_instagram_video_with_centered_image, delete_file, create_instagram_video_with_repeating_video, create_video_with_repeating_video
from src.yt.utils import initialize_upload, resumable_upload
from src.states import CreateNew, CreateVideo, CreateVideoFromVideo, PublishVideo, Connect
import asyncio
import os
import uuid
import requests
from aiogram.fsm.context import FSMContext

router = Router()
global_state = {}

@router.callback_query(F.data == "start")
async def start_callback_handler(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Нажми на /start, если подписался")

@router.callback_query(lambda query: query.data in ['yt_video', 'ig_video'])
async def process_callback_video_type(callback_query: CallbackQuery):
    answer = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if chat_id in global_state:
        if answer == 'yt_video':
            await create_video_from_video_for_youtube(callback_query.message)
        elif answer == 'ig_video':
            await create_video_from_video_for_instagram(callback_query.message)

@router.callback_query(lambda query: query.data in ['yt_photo', 'ig_photo'])
async def process_callback_photo_type(callback_query: CallbackQuery):
    answer = callback_query.data
    chat_id = callback_query.message.chat.id
    
    if chat_id in global_state:
        if answer == 'yt_photo':
            await create_video_for_youtube(callback_query.message)
        elif answer == 'ig_photo':
            await create_video_for_instagram(callback_query.message)

@router.message(CommandStart())
async def cmd_start(message: Message):
    chat_id = "@seamusicmgmt"
    chat_member = await message.bot.get_chat_member(chat_id, message.from_user.id)
    
    # backend_url = "http://127.0.0.1:8000/v1/subscription/telegram/"

    # params = {
    #     "telegram_id": message.from_user.id
    # }
    # response = requests.get(backend_url, params=params)
    # print(response)

    # if response.status_code == 404:
    #     create_response = requests.post(backend_url, data=params)
    #     if create_response.status_code == 201:
    #         print("Акаунт успешно создан!")
    #     else:
    #         print("Ошибка при создании аккаунта:", create_response.status_code)
    # else:
    #     print("Аккаунт получен:", response.json())

    if chat_member.status in ["member", "administrator", "creator"]:
        caption = f"Привет, {message.from_user.username}! Создано разработчиком @whyspacy как часть проекта @seamusicmgmt. Бот может создавать видео из mp3 и изображения или видео (зацикливая его на всю продолжительность аудио), а затем при желании вы можете выложить видео на ютуб НАПРЯМУЮ из этого телеграм бота.\n\n/start - перезапустить \n/profile - ваш профиль\n/create - создать видео\n/help - все комманды \n"
        photo = FSInputFile("fasttube.jpg")
        await message.answer_photo(photo=photo, caption=caption)
    else:
        await message.answer("Для начала работы бота, нужно подписаться на канал проекта", reply_markup=project_channel)

async def send_newsletter(message: Message, all_users):
    for user_id in all_users:
        await message.bot.send_photo(user_id, photo=message.photo[-1].file_id, caption=message.caption)

@router.message(Command("new"))
async def forward_message(message: Message, state: FSMContext):
    if message.from_user.username == "spxcyyy":
        await message.answer("Теперь отправляй новость")
        await state.set_state(CreateNew.is_continue)

@router.message(CreateNew.is_continue, F.photo)
async def forward_message(message: Message):
    if message.from_user.username == "spxcyyy":
        all_users = []
        
        url = "http://127.0.0.1:8000/subscription/telegram/"
        response = requests.get(url)
        print(response.json())
        for id in response.json():
            all_users.append(id)

        await send_newsletter(message, all_users)

@router.message(Command("help"))
async def cmd_message(message: Message):
    await message.answer("\n/start - Перезапустить \n/create_with_photo - Создать видео из фото\n/create_with_video - Создать зацикливающееся видео\n/connect - Подключить свой ютуб канал /security - Почему это безопасно \n/upload - Загрузить видео на ютуб \n/seamusic - Аккаунт SEAMUSIC | ? \n/profile - Ваш профиль")

@router.message(Command("create_with_photo"))
async def create_video(message: Message, state: FSMContext):
    await message.answer("Для начала процесса создания видео, скиньте качественное изображение для того вида видео, которое хотите получить.")
    await state.set_state(CreateVideo.image)

@router.message(CreateVideo.image, F.photo)
async def get_photo(message: Message):
    
    chat_id = message.chat.id
    if chat_id not in global_state:
        global_state[chat_id] = {}  # Initialize global_state for the chat_id if it doesn't exist

    file_id = message.photo[-1].file_id
    global_state[chat_id]["photo_id"] = await download_and_save_photo(message, file_id)
    await message.answer("Изображение успешно загружено! Теперь скиньте аудиофайл исключительно формата mp3.")

async def download_and_save_photo(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    photo_path = f"temp_photo_{uuid.uuid4()}"
    with open(photo_path, "wb") as photo_file:
        photo_file.write(downloaded_file.read())
    return photo_path

@router.message(CreateVideo.image, F.audio)
async def get_audio(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        photo_path = global_state[chat_id]["photo_id"]
        audio_file_id = message.audio.file_id
        audio_path = await download_and_save_audio(message, audio_file_id)
        global_state[chat_id] = {"photo_path": photo_path, "audio_path": audio_path}
        await message.answer("Выберите формат видео: ", reply_markup=yt_or_inst_for_photo_type)
    else:
        await message.answer("Для создания видео загрузи сначала изображение, а затем аудиофайл.")

@router.message(Command("create_with_video"))
async def create_video_from_video(message: Message, state: FSMContext):
    await message.answer("Для начала процесса создания видео, скиньте качественный видео файл для того вида видео, которое хотите получить.")
    await state.set_state(CreateVideoFromVideo.video)

@router.message(CreateVideoFromVideo.video, F.video)
async def get_video_for_video_from_video(message: Message):
    
    chat_id = message.chat.id
    if chat_id not in global_state:
        global_state[chat_id] = {}

    file_id = message.video.file_id
    global_state[chat_id]["video_id"] = await download_and_save_video(message, file_id)
    await message.answer("Видео файл успешно загружен! Теперь скиньте аудиофайл исключительно формата mp3.")

async def download_and_save_video(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    video_path = f"temp_video_{uuid.uuid4()}"
    with open(video_path, "wb") as video_file:
        video_file.write(downloaded_file.read())
    return video_path

@router.message(CreateVideoFromVideo.video, F.audio)
async def get_audio_for_video_from_video(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        video_path = global_state[chat_id]["video_id"]
        audio_file_id = message.audio.file_id
        audio_path = await download_and_save_audio(message, audio_file_id)
        global_state[chat_id] = {"video_path": video_path, "audio_path": audio_path}
        await message.answer("Выберите формат видео: ", reply_markup=yt_or_inst_for_video_type)
    else:
        await message.answer("Для создания видео загрузи видео файл, а затем аудиофайл.")

async def create_video_from_video_for_youtube(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для ютубе! Обычно процесс занимает 1-2 минуты")

        video_path = global_state[chat_id]["video_path"]
        audio_path = global_state[chat_id]["audio_path"]

        video_data = await create_video_with_repeating_video(audio_path, video_path)

        await message.answer("Успешно!")

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input)
        await message.answer("Теперь вы можете загрузить его на ютуб по команде /upload")
        await delete_file(video_data["video_path"])
        await delete_file(video_path)
        await delete_file(audio_path)

async def create_video_from_video_for_instagram(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для инстраграма! Обычно процесс занимает 1-2 минуты")

        video_path = global_state[chat_id]["video_path"]
        audio_path = global_state[chat_id]["audio_path"]

        video_data = await create_instagram_video_with_repeating_video(audio_path, video_path)

        await message.answer("Успешно!")

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input)
        await message.answer("Теперь вы можете загрузить его на ютуб по команде /upload")
        await delete_file(video_data["video_path"])
        await delete_file(video_path)
        await delete_file(audio_path)


async def create_video_for_youtube(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для ютубе! Обычно процесс занимает 1-2 минуты")

        photo_path = global_state[chat_id]["photo_path"]
        audio_path = global_state[chat_id]["audio_path"]

        video_data = await create_video_with_stretched_image(audio_path, photo_path)

        await message.answer("Успешно!")

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input)
        await message.answer("Теперь вы можете загрузить его на ютуб по команде /upload")
        await delete_file(video_data["video_path"])
        await delete_file(photo_path)
        await delete_file(audio_path)

async def create_video_for_instagram(message: Message):
    chat_id = message.chat.id
    if chat_id in global_state:
        await message.answer("Началось создание видео для инстраграма! Обычно процесс занимает 1-2 минуты")

        photo_path = global_state[chat_id]["photo_path"]
        audio_path = global_state[chat_id]["audio_path"]

        video_data = await create_instagram_video_with_centered_image(audio_path, photo_path)

        await message.answer("Успешно!")

        video_input = FSInputFile(video_data["video_path"])
        await message.answer_video(video_input)
        await message.answer("Теперь вы можете загрузить его на ютуб по команде /upload")
        await delete_file(video_data["video_path"])
        await delete_file(photo_path)
        await delete_file(audio_path)

async def download_and_save_audio(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    audio_path = f"temp_audio_{uuid.uuid4()}"
    with open(audio_path, "wb") as audio_file:
        audio_file.write(downloaded_file.read())
    return audio_path


@router.message(Command("connect"))
async def connect_command(message: Message, state: FSMContext):
    await message.answer("При нажатии на ссылку откроется страница авторизация Google, вам нужно будет выбрать тот канал на который должны будут выкладываться видео. Если вдруг высветится страница 'Эксперты Google не проверяли это приложение', то нужно нажать 'Дополнительные настройки' и нажать 'Перейти на страницу FASTTUBE (небезопасно)' \n Почему так происходит? Мы не можем получить одобрение от гугл по проверке телеграм бота, с этим, темболее из России будут возникать большие сложности.")
    
    url = f"http://127.0.0.1:8000/subscription/auth_link"
    response = requests.get(url)
    data = response.json()

    await message.answer(f"Cсылка: {data['auth_link']}, после ")
    await state.set_state(Connect.credentials)

@router.message(Connect.credentials)
async def connect_command(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await message.answer("При нажатии на ссылку откроется страница авторизация Google, вам нужно будет выбрать тот канал на который должны будут выкладываться видео. Если вдруг высветится страница 'Эксперты Google не проверяли это приложение', то нужно нажать 'Дополнительные настройки' и нажать 'Перейти на страницу FASTTUBE (небезопасно)' \n Почему так происходит? Мы не можем получить одобрение от гугл по проверке телеграм бота, с этим, темболее из России будут возникать большие сложности.")
    
    url = f"http://127.0.0.1:8000/subscription/auth_link"
    response = requests.get(url)
    data = response.json()

    await message.answer(f"Cсылка: {data.auth_link}")
    global_state[chat_id] = {"credentials": response.json()}
    
    await message.answer("Поздравляю! Вы подключили свой ютуб канал, теперь можете выложить видео. /upload")
    await state.set_state(Connect.credentials)


@router.message(Command("upload"))
async def upload_command(message: Message):
    chat_id = message.chat.id
    
    if "credentials" in global_state.get(chat_id, {}): 
        credentials = global_state[chat_id]["credentials"]

        await message.answer(f"Отправьте или репостните видео сделанное этим ботом ранее.")
    else:
        await message.answer("Для начала загрузки видео, нужно подключить свой ютуб канал /connect. Если вы беспокоитесь за ваши данные и безопасность - /security")

async def download_and_save_video(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    video_path = f"any_video_{os.path.basename(file_path)}"
    with open(video_path, "wb") as video_file:
        video_file.write(downloaded_file.read())
    return video_path

@router.message(F.video)
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

@router.message(PublishVideo.title, F.text)
async def get_video_title(message: Message, state: FSMContext):
    chat_id = message.chat.id
    global_state[chat_id]["video_title"] = message.text
    await message.answer(f"Название: {message.text}, теперь напишите описание.")
    await state.set_state(PublishVideo.description)

@router.message(PublishVideo.description, F.text)
async def get_video_tags(message: Message, state: FSMContext):
    chat_id = message.chat.id
    global_state[chat_id]["video_description"] = message.text
    await message.answer(f"Описание: {message.text}, теперь введите теги для видео. Пример: музыка, type beat, ken karson и т.п.", parse_mode="MarkdownV2")
    await state.set_state(PublishVideo.tags)

@router.message(PublishVideo.tags, F.text)
async def get_confirm_video(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if "credentials" in global_state.get(chat_id, {}):  # Проверяем наличие ключа "credentials" в словаре global_state[chat_id]
        global_state[chat_id]["video_tags"] = message.text
        await message.answer(f"Окей, для подтверждения загрузки, введите комманду /publish.")
        await state.set_state(PublishVideo.confirm)

@router.message(PublishVideo.confirm, F.text)
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



@router.message(Command("security"))
async def security_command(message: Message):
    await message.answer("If you doubt the security of connecting your account, we use oauth 2.0 (you can Google it to be absolutely sure) to authorize your Google account in our bot. this means that your personal data is not shared directly with the bot. Instead, Google's system gives the bot access to the information it needs without revealing your actual password. We only request the permissions necessary to perform the bot's functions, thereby minimizing access to your data. + you can always adjust and track all actions on your account")


@router.message(Command("profile"))
async def profile_command(message: Message):
    caption = f"Профиль FASTTUBE пользователя @{message.from_user.username}\n\nЮтуб канал: Есть | Подключить - /connect\nБаланс (рублей): 8234р.\nДрузья: 23\nРеферальная ссылка для приглашений друзей: https://fasttubesmbot?start={message.from_user.id} | Кол-во рефералов: 0\nПримиум: Есть | /premium\n\nАккаунт SEAMUSIC: TRUE | /seamusic \nВсе комманды - /help"
    photo = FSInputFile("fasttube.jpg")
    await message.answer_photo(photo=photo, caption=caption)