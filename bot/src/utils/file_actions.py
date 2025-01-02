import os
import uuid
from moviepy.editor import VideoFileClip
from aiofiles import open as aio_open


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
    
    # Save the downloaded file to a temporary file
    async with aio_open(temp_video_path, "wb") as video_file:
        await video_file.write(downloaded_file.read())

    # Check the file size
    file_size = os.path.getsize(temp_video_path)
    if file_size > 100 * 1024 * 1024:  # 100 MB in bytes
        os.remove(temp_video_path)  # Remove the temporary file
        return "Error: The file is larger than 100 MB and cannot be processed."

    # Check if the file is a video and convert to MP4
    try:
        clip = VideoFileClip(temp_video_path)
        mp4_video_path = f"{directory}temp_video_{uuid.uuid4()}.mp4"
        clip.write_videofile(mp4_video_path, codec='libx264')
    except Exception as e:
        os.remove(temp_video_path)  # Remove the temporary file in case of error
        return f"Error: The file is not a valid video or cannot be processed. Details: {str(e)}"
    finally:
        clip.close()  # Ensure the clip is closed properly

    # Remove the temporary file after processing
    os.remove(temp_video_path)

    return mp4_video_path