from fastapi import Cookie, Depends
from jose import JWTError, jwt, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import utils as auth_utils
from app.auth.config import auth_config, oauth2_scheme
from app.auth.exceptions import (AuthorizationFailed, AuthRequired, AccessTokenRequired,
                                 InvalidToken, RefreshTokenNotValid, AccessTokenExpired)
from app.auth.schemas import JWTData
from app.auth.service import TokenService
from app.database import get_db
from app.users.models import UserModel, UserRole
from app.users.service import UserService


async def get_user_from_refresh_token(
    db: AsyncSession = Depends(get_db),
    refresh_token_value: str = Cookie(..., alias="refreshToken"),
    token_service: TokenService = Depends(TokenService),
    user_service: UserService = Depends(UserService),
) -> UserModel:
    """
    Retrieves a user from the database using a refresh token. 

    Args:
        db (AsyncSession): Async database session
        db_refresh_token (RefreshToken): The refresh token from the database
        user_service (UserService): User manager dependency

    Returns:
        User: The corresponding user from the database
    """

    refresh_token = await token_service.get_refresh_token_by_value(
        db, refresh_token_value
    )

    if not refresh_token:
        raise RefreshTokenNotValid()

    if auth_utils.is_refresh_token_expired(refresh_token):
        raise RefreshTokenNotValid()

    user_id = refresh_token.user_id
    db_user = await user_service.get_by_id(db, user_id)

    if not db_user:
        raise RefreshTokenNotValid()

    return db_user


async def get_admin_from_refresh_token(
    user: UserModel = Depends(get_user_from_refresh_token),
) -> UserModel:
    """
    Retrieves the admin user from a refresh token.

    Args:
        user (User): The user from the refresh token

    Returns:
        User: The admin user

    Raises:
        AuthorizationFailed: If the user is not an admin
    """

    if user.role != UserRole.ADMIN:
        raise AuthorizationFailed()

    return user


async def get_user_from_access_token(
    db: AsyncSession = Depends(get_db),
    access_token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(UserService),
) -> UserModel:
    """
    Retrieves a user by access token.

    Args:
        db (AsyncSession): The async session for database operations.
        access_token (str): The access token for authentication.
        user_service (UserService): The user manager for user-related operations.

    Returns:
        User: The user corresponding to the provided access token.

    Raises:
        AuthRequired: If access token is missing or invalid, or user is not found.
        InvalidToken: If the access token is invalid.
    """

    if not access_token:
        raise AccessTokenRequired()

    try:
        payload = jwt.decode(
            access_token, 
            auth_config.JWT_SECRET, 
            algorithms=[auth_config.JWT_ALG]
        )
    except ExpiredSignatureError:
        raise AccessTokenExpired()
    except JWTError:
        raise InvalidToken()

    jwt_token: JWTData = JWTData(**payload)

    if not jwt_token:
        raise InvalidToken()
    
    user_id = jwt_token.user_id
    user_db = await user_service.get_by_id(db, user_id)

    if not user_db:
        raise AuthRequired()

    return user_db

# ??? do I need it
async def get_admin_from_access_token(
    user: UserModel = Depends(get_user_from_access_token),
) -> UserModel:
    """
    Retrieves the admin user from a access token.

    Args:
        user (User): The user from the access token

    Returns:
        User: The admin user

    Raises:
        AuthorizationFailed: If the user is not an admin
    """

    if user.role != UserRole.ADMIN:
        raise AuthorizationFailed()

    return user
