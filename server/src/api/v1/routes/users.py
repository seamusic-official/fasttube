from fastapi import HTTPException, APIRouter
from typing import Optional, List
from src.repositories.auth import UserRepository
from src.api.v1.schemas.users import UserResponse, UserCreate, UserUpdate


router = APIRouter(prefix="/users", tags=["Auth & Users"])a

@router.post("", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    new_user = await UserRepository.add_user(user.username, user.full_name, user.telegram_id)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int):
    user = await UserRepository.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("", response_model=List[UserResponse])
async def list_users(username: Optional[str] = None, full_name: Optional[str] = None, telegram_id: Optional[str] = None):
    filters = {k: v for k, v in {"username": username, "full_name": full_name, "telegram_id": telegram_id}.items() if v is not None}
    users = await UserRepository.get_users_with_filters(**filters)
    return users

@router.get("/all", response_model=List[UserResponse])
async def get_all_users():
    return await UserRepository.get_scalars_users()

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    updated_user = await UserRepository.update_user(user_id, **user_update.dict(exclude_unset=True))
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    await UserRepository.delete_user(user_id)
    return {"detail": "User deleted successfully"}