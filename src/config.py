import os
from typing import Union
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv(os.path.join(os.path.dirname(__file__), 'fasttube', '.env'))


class TelegramSettings(BaseModel):
    TELEGRAM_API_KEY: str = os.environ.get("TELEGRAM_API_KEY")

class DbSettings(BaseModel):
    url: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"



class Settings(BaseSettings):
    
    api_v1_prefix: str = "/api/v1"
    
    telegram: TelegramSettings = TelegramSettings()
    db: DbSettings = DbSettings()



settings = Settings()