import os
import uuid
import pytest
import asyncio
from moviepy import AudioFileClip
from PIL import Image
from src.utils.moviepy import create_video_with_stretched_image  # Замени your_module на имя твого файла

@pytest.fixture
def setup_audio_file(tmpdir):
    # Создаем временный аудиофайл для тестов
    audio_path = tmpdir.join("test_audio.mp3")
    # Здесь можно записать или скопировать тестовый аудиофайл
    # Например, создадим пустой файл
    with open(audio_path, 'wb') as f:
        f.write(b'0' * 1024)  # Записи 1КБ данных
    return str(audio_path)

@pytest.fixture
def setup_image_file(tmpdir):
    # Создаем временное изображение для тестов
    image_path = tmpdir.join("test_image.jpg")
    image = Image.new("RGB", (800, 600), color=(255, 0, 0))  # Создаем красное изображение
    image.save(image_path)
    return str(image_path)

@pytest.mark.asyncio
async def test_create_video_with_stretched_image(setup_audio_file, setup_image_file):
    audio_path = setup_audio_file
    photo_path = setup_image_file
    
    result = await create_video_with_stretched_image(audio_path, photo_path)

    # Проверяем, что видео файл создан
    assert "video_path" in result
    assert os.path.exists(result["video_path"])

    # Проверяем, что продолжительность совпадает с длиной аудио
    audio = AudioFileClip(audio_path)
    assert result["duration"] == audio.duration

    # Удаляем созданный видеофайл после теста
    os.remove(result["video_path"])

@pytest.mark.asyncio
async def test_create_video_with_invalid_audio(setup_image_file):
    photo_path = setup_image_file
    invalid_audio_path = "invalid_audio.mp3"  # Не существует

    # Проверяем, что функция выбрасывает ошибку
    with pytest.raises(Exception):
        await create_video_with_stretched_image(invalid_audio_path, photo_path)

@pytest.mark.asyncio
async def test_create_video_with_invalid_image(setup_audio_file):
    audio_path = setup_audio_file
    invalid_image_path = "invalid_image.jpg"  # Не существует

    # Проверяем, что функция выбрасывает ошибку
    with pytest.raises(Exception):
        await create_video_with_stretched_image(audio_path, invalid_image_path)