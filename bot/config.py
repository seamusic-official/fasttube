import os
from typing import Union
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()

class TelegramSettings(BaseModel):
    TELEGRAM_API_KEY: str = os.environ.get("TELEGRAM_API_KEY")

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    telegram: TelegramSettings = TelegramSettings()

settings = Settings()