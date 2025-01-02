from pydantic import BaseModel
from typing import Optional, List

class UserCreate(BaseModel):
    username: str
    full_name: str
    telegram_id: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    full_name: Optional[str] = None
    telegram_id: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    telegram_id: str