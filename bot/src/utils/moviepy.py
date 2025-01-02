import logging
from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips, ImageClip, ColorClip, CompositeVideoClip
from PIL import Image
import numpy as np

import asyncio
import uuid
import os


async def create_video_with_stretched_image(audio_path, photo_path):
    try:
        audio = AudioFileClip(audio_path)
        if audio is None:
            logging.error("AudioFileClip returned None.")
            return None
    except Exception as e:
        logging.error("Error loading audio: %s", str(e), exc_info=True)
        return None
    
    try:
        image = Image.open(photo_path)
        if image is None:
            logging.error("Image.open returned None.")
            return None
    except Exception as e:
        logging.error("Error loading image: %s", str(e), exc_info=True)
        return None
    
    aspect_ratio = image.width / image.height
    desired_height = 1080
    desired_width = int(desired_height * aspect_ratio)
    image = image.resize((desired_width, desired_height))
    
    x_position = (1920 - desired_width) // 2
    y_position = 0
    
    background_clip = ColorClip((1920, 1080), color=[0, 0, 0], duration=audio.duration)
    if background_clip is None:
        logging.error("ColorClip returned None.")
        return None
    
    image_np = np.array(image)
    image_clip = ImageClip(image_np).set_duration(audio.duration).set_position((x_position, y_position))
    if image_clip is None:
        logging.error("ImageClip returned None.")
        return None
    
    final_clip = CompositeVideoClip([background_clip, image_clip]).set_audio(audio)
    if final_clip is None:
        logging.error("CompositeVideoClip returned None.")
        return None

    directory = "youtube-videos/"
    if not os.path.exists(directory):
        os.makedirs(directory)

    video_path = f"{directory}youtube-video-{uuid.uuid4()}.mp4"
    
    try:
        await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')
    except Exception as e:
        logging.error("Error creating video: %s", str(e), exc_info=True)
        return None
    
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
    try:
        audio = AudioFileClip(audio_path)
    except Exception as e:
        logging.error("Error loading audio file: %s", str(e), exc_info=True)
        return None
    
    try:
        video = VideoFileClip(video_path)
    except Exception as e:
        logging.error("Error loading video file: %s", str(e), exc_info=True)
        return None
    
    loops_needed = int(audio.duration / video.duration) + 1
    repeated_video = concatenate_videoclips([video] * loops_needed)

    final_video = repeated_video.subclip(0, audio.duration)
    
    x_position = 'center'
    y_position = 'center'

    background_clip = ColorClip((1920, 1080), color=[0, 0, 0], duration=audio.duration)
    final_clip = CompositeVideoClip([background_clip, final_video.set_position((x_position, y_position))])
    final_clip = final_clip.set_audio(audio)
    
    directory = "youtube-repeating-videos/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    video_output_path = f"{directory}youtube-repeating-video-{uuid.uuid4()}.mp4"
    
    try:
        await asyncio.to_thread(final_clip.write_videofile, video_output_path, fps=24, codec='libx264')
    except Exception as e:
        logging.error("Error writing video file: %s", str(e), exc_info=True)
        return None
    
    return {"video_path": video_output_path, "duration": audio.duration}

async def create_instagram_video_with_repeating_video(audio_path, video_path):
    audio = AudioFileClip(audio_path)
    video = VideoFileClip(video_path)

    loops_needed = int(audio.duration / video.duration) + 1
    repeated_video = concatenate_videoclips([video] * loops_needed)

    final_video = repeated_video.subclip(0, audio.duration)

    background_clip = ColorClip((1080, 1920), color=[0, 0, 0], duration=audio.duration)
    
    x_position = 'center'
    y_position = 'center'

    final_clip = CompositeVideoClip([background_clip, final_video.set_position((x_position, y_position))])
    final_clip = final_clip.set_audio(audio)
    
    directory = "instagram-repeating-videos/"

    if not os.path.exists(directory):
        os.makedirs(directory)
    
    video_output_path = f"{directory}instagram-repeating-video-{uuid.uuid4()}.mp4"
    
    await asyncio.to_thread(final_clip.write_videofile, video_output_path, fps=24, codec='libx264')
    return {"video_path": video_output_path, "duration": audio.duration}

