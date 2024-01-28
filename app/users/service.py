from datetime import datetime

from asyncpg.exceptions import UniqueViolationError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.utils import check_password, hash_password
from app.users import schemas
from app.users.models import UserModel


class UserService:

    async def create_user(
        self,
        db: AsyncSession,
        user: schemas.User,
    ) -> UserModel:
        """
        Creates a new user in the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            user (schemas.User): The user data to be created.

        Returns:
            UserModel: The created user.
        """

        new_user = UserModel(
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            created_at=datetime.utcnow(),
            role=user.role,
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    async def get_by_id(self, db: AsyncSession, user_id: int) -> UserModel | None:
        """
        Retrieves a user by their ID from the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserModel | None: The user with the specified ID, or None if not found.
        """

        result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
        user = result.scalars().first()

        return user

    async def get_by_username(
        self, db: AsyncSession, username: str
    ) -> UserModel | None:
        """
        Retrieves a user by username from the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            username (str): The username of the user to retrieve.

        Returns:
            UserModel | None: The user model if found, else None.
        """

        result = await db.execute(
            select(UserModel).filter(UserModel.username == username)
        )
        user = result.scalars().first()

        return user
    
    async def get_by_email(self, db: AsyncSession, email: str) -> UserModel | None:
        """
        Retrieves a user by email from the database.

        Args:
            db (AsyncSession): The asynchronous database session.
            email (str): The email of the user to retrieve.

        Returns:
            UserModel | None: The user model if found, else None.
        """

        result = await db.execute(select(UserModel).filter(UserModel.email == email))
        user = result.scalars().first()

        return user

    async def authenticate(
        self,
        db: AsyncSession,
        form_data: OAuth2PasswordRequestForm,
    ) -> UserModel | None:
        """
        Asynchronously authenticate a user using the provided OAuth2PasswordRequestForm.

        Args:
            db (AsyncSession): The asynchronous database session.
            form_data (OAuth2PasswordRequestForm): The OAuth2PasswordRequestForm to authenticate.

        Returns:
            UserModel | None: The authenticated user, or None if authentication fails.
        """

        user = await self.get_by_username(db, form_data.username)

        if not user or not check_password(form_data.password, user.password):
            return None

        return user
