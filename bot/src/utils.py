from moviepy.editor import AudioFileClip, ImageClip, ffmpeg_tools
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import CompositeAudioClip, AudioFileClip, ColorClip, CompositeVideoClip
from PIL import Image
from moviepy.editor import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip
import numpy as np
import asyncio
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

async def authenticate():
    """
    Create an authenticated service to interact with the YouTube API
    """
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no valid credentials, ask the user to authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_537737694718-u7hvual5hlrehrpce7425htfdm74ba6q.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
    
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build the YouTube service
    return build('youtube', 'v3', credentials=creds)

def upload_video(youtube, file_path, title, description, tags=[]):
    """
    Upload a video to YouTube
    """
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags
        },
        'status': {
            'privacyStatus': 'private'  # You can set this to 'public' as well
        }
    }

    media_file = MediaFileUpload(file_path)

    youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media_file
    ).execute()
    
# Make sure to handle exceptions, input sanitization, and user authorization in your bot implementation

# Example usage:
# youtube = create_authenticated_service()
# upload_video(youtube, 'video.mp4', 'My Video Title', 'Awesome description', ['tag1', 'tag2'])

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

    video_path = "output_video_with_centered_image.mp4"
    await asyncio.to_thread(final_clip.write_videofile, video_path, fps=24, codec='libx264')

    return {"video_path": video_path, "duration": audio.duration}