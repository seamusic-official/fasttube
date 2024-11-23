import logging
from moviepy import *
from PIL import Image
import numpy as np

import asyncio
import uuid
import os


async def create_video_with_stretched_image(audio_path, photo_path):
    # Загружаем аудио
    audio = AudioFileClip(audio_path)
    
    # Загружаем изображение и изменяем его размер
    image = Image.open(photo_path)
    aspect_ratio = image.width / image.height
    desired_height = 1080
    desired_width = int(desired_height * aspect_ratio)
    image = image.resize((desired_width, desired_height))
    
    x_position = (1920 - desired_width) // 2
    y_position = 0
    
    background_clip = ColorClip((1920, 1080), color=[0, 0, 0], duration=audio.duration)
    
    image_np = np.array(image)

    image_clip = ImageClip(image_np).duration(audio.duration)
    image_clip = ImageClip(image_np).pos([x_position, y_position])
    
    final_clip = CompositeVideoClip([background_clip, image_clip]).audio(audio)

    directory = "youtube-videos/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    video_path = f"{directory}youtube-video-{uuid.uuid4()}.mp4"
    
    try:
        await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')
    except Exception as e:
        logging.error("Ошибка при создании видео: %s", str(e), exc_info=True)
        
    return {"video_path": video_path, "duration": audio.duration}


async def create_instagram_video_with_centered_image(audio_path, photo_path):
    audio = AudioFileClip(audio_path)
    image = Image.open(photo_path)

    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    aspect_ratio = image.width / image.height
    desired_width = 1080
    desired_height = int(desired_width / aspect_ratio)
    image = image.resize((desired_width, desired_height))
    
    x_position = (1080 - desired_width) // 2
    y_position = (1920 - desired_height) // 2
    
    background_clip = ColorClip((1080, 1920), color=[0, 0, 0], duration=audio.duration)
    
    image_np = np.array(image)
    image_clip = ImageClip(image_np, duration=audio.duration)
    
    image_clip = image_clip.set_duration(audio.duration)
    image_clip = image_clip.set_fps(24)
    image_clip = image_clip.set_position((x_position, y_position))
    
    final_clip = CompositeVideoClip([background_clip, image_clip])
    final_clip = final_clip.set_audio(audio)
    
    directory = "instagram-videos/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    video_path = f"{directory}instagram-video-{uuid.uuid4()}.mp4"
    await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')
    
    return {"video_path": video_path, "duration": audio.duration}


async def create_video_with_repeating_video(audio_path, video_path):
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path)
    
    loops_needed = int(audio.duration / video.duration) + 1
    repeated_video = concatenate_videoclips([video] * loops_needed)

    final_video = repeated_video.subclip(0, audio.duration)
    
    background_clip = ColorClip((1920, 1080), color=[0, 0, 0], duration=audio.duration)
    final_clip = CompositeVideoClip([background_clip, final_video.set_position(("center"))])
    final_clip = final_clip.set_audio(audio)
    
    directory = "youtube-repeating-videos/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    video_output_path = f"{directory}youtube-repeating-video-{uuid.uuid4()}.mp4"
    await asyncio.to_thread(final_clip.write_videofile, video_output_path, fps=24, codec='libx264')
    return {"video_path": video_output_path, "duration": audio.duration}

async def create_instagram_video_with_repeating_video(audio_path, video_path):
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path)

    loops_needed = int(audio.duration / video.duration) + 1
    repeated_video = concatenate_videoclips([video] * loops_needed)

    final_video = repeated_video.subclip(0, audio.duration)

    background_clip = ColorClip((1080, 1920), color=[0, 0, 0], duration=audio.duration)

    final_clip = CompositeVideoClip([background_clip, final_video.set_position(("center"))])
    final_clip = final_clip.set_audio(audio)
    
    directory = "instagram-repeating-videos/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    video_output_path = f"{directory}instagram-repeating-video-{uuid.uuid4()}.mp4"
    
    await asyncio.to_thread(final_clip.write_videofile, video_output_path, fps=24, codec='libx264')
    return {"video_path": video_output_path, "duration": audio.duration}

