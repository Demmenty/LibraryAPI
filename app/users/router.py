from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependiencies import (
    get_admin_from_refresh_token,
    get_user_from_refresh_token,
)
from app.database import get_db
from app.users.exceptions import EmailTaken, UsernameTaken
from app.users.models import UserModel
from app.users.schemas import User, UserResponse
from app.users.service import UserService

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(
    new_user: User,
    db: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(UserService),
    admin: UserModel = Depends(get_admin_from_refresh_token),
) -> dict:
    """
    Only for admins.
    Create a new user with the provided credentials and role.
    """

    if await user_service.get_by_email(db, new_user.email):
        raise EmailTaken()

    if await user_service.get_by_username(db, new_user.username):
        raise UsernameTaken()

    user = await user_service.create_user(db, new_user)

    return user


@router.get("/me", response_model=UserResponse)
async def get_me(user: UserModel = Depends(get_user_from_refresh_token)) -> dict:
    """Get the logged user information"""

    return user
