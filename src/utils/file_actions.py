import os
import uuid
from moviepy.editor import VideoFileClip


async def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Успешно удалено видео по пути: {file_path}")
    except OSError as e:
        print(f"Ошибка при удалении видео: {e}")

async def download_and_save_photo(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    directory = "media/temp-photo/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    photo_path = f"{directory}temp_photo_{uuid.uuid4()}"

    with open(photo_path, "wb") as photo_file:
        photo_file.write(downloaded_file.read())
    return photo_path


async def download_and_save_audio(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    directory = "media/temp-audio/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    audio_path = f"{directory}temp_audio_{uuid.uuid4()}"

    with open(audio_path, "wb") as audio_file:
        audio_file.write(downloaded_file.read())
    return audio_path


async def download_and_save_video(message, file_id):
    file_path = (await message.bot.get_file(file_id)).file_path
    downloaded_file = await message.bot.download_file(file_path)
    directory = "media/temp-video/"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    temp_video_path = f"{directory}temp_video_{uuid.uuid4()}"
    
    with open(temp_video_path, "wb") as video_file:
        video_file.write(downloaded_file.read())

    mp4_video_path = f"{directory}temp_video_{uuid.uuid4()}.mp4"
    
    clip = VideoFileClip(temp_video_path)
    clip.write_videofile(mp4_video_path, codec='libx264')

    return mp4_video_path
