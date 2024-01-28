from fastapi import APIRouter, Depends

from app.auth.dependiencies import get_user_from_refresh_token
from app.users.models import UserModel
from app.users.schemas import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(user: UserModel = Depends(get_user_from_refresh_token)) -> dict:
    """Get the logged user information"""

    return user
