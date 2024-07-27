from moviepy.editor import AudioFileClip, ImageClip, ffmpeg_tools
from moviepy.editor import CompositeAudioClip, AudioFileClip, ColorClip, CompositeVideoClip
from PIL import Image
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
import numpy as np
import asyncio
import os
import uuid


async def create_video_with_stretched_image(audio_path, photo_path):
    # Load the audio
    audio = AudioFileClip(audio_path)

    # Determine the aspect ratio of the original image
    image = Image.open(photo_path)
    aspect_ratio = image.width / image.height

    # Calculate the desired height and width for the image to fill the video frame
    desired_height = 1080
    desired_width = int(desired_height * aspect_ratio)

    # Resize the image to fill the frame while maintaining aspect ratio
    image = image.resize((desired_width, desired_height))

    # Calculate the position to center the image horizontally
    x_position = (1920 - desired_width) // 2
    y_position = 0  # Adjust vertical position if needed

    # Create a black background clip
    background_clip = ColorClip((1920, 1080), color=[0, 0, 0], duration=audio.duration)

    # Convert the resized image to NumPy array
    image_np = np.array(image)

    # Create ImageClip from the resized image
    image_clip = ImageClip(image_np, duration=audio.duration)
    image_clip = image_clip.set_duration(audio.duration)
    image_clip = image_clip.set_fps(24)
    image_clip = image_clip.set_position((x_position, y_position))

    # Position the image on top of the black background
    final_clip = CompositeVideoClip([background_clip, image_clip])

    # Set audio for the video
    final_clip = final_clip.set_audio(audio)

    video_path = f"youtube-video-{uuid.uuid4()}.mp4"
    await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')

    return {"video_path": video_path, "duration": audio.duration}

async def create_instagram_video_with_centered_image(audio_path, photo_path):
    # Load the audio
    audio = AudioFileClip(audio_path)

    # Determine the aspect ratio of the original image
    image = Image.open(photo_path)
    aspect_ratio = image.width / image.height

    # Calculate the desired width and height for the image to fill the vertical frame
    desired_width = 1080
    desired_height = int(desired_width / aspect_ratio)

    # Resize the image while maintaining aspect ratio
    image = image.resize((desired_width, desired_height))

    # Calculate the position to center the image vertically
    x_position = (1080 - desired_width) // 2
    y_position = (1920 - desired_height) // 2

    # Create a black background clip
    background_clip = ColorClip((1080, 1920), color=[0, 0, 0], duration=audio.duration)

    # Convert the resized image to NumPy array
    image_np = np.array(image)

    # Create ImageClip from the resized image
    image_clip = ImageClip(image_np, duration=audio.duration)
    image_clip = image_clip.set_duration(audio.duration)
    image_clip = image_clip.set_fps(24)
    image_clip = image_clip.set_position((x_position, y_position))

    # Position the image on top of the black background
    final_clip = CompositeVideoClip([background_clip, image_clip])
    
    # Set audio for the video
    final_clip = final_clip.set_audio(audio)

    video_path = f"inst-or-ytshorts-or-tiktok-video-{uuid.uuid4()}.mp4"
    await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')

    return {"video_path": video_path, "duration": audio.duration}


async def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Успешно удалено видео по пути: {file_path}")
    except OSError as e:
        print(f"Ошибка при удалении видео: {e}")