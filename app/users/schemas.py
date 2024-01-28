import enum

from pydantic import BaseModel as BaseSchema
from pydantic import EmailStr, Field, field_validator


class MembershipStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseSchema):
    username: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: UserRole = UserRole.USER

    @field_validator("password", mode="after")
    @classmethod
    def check_password(cls, password: str) -> str:
        from app.auth.utils import is_strong_password

        if not is_strong_password(password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or special symbol"
            )

        return password


class UserResponse(BaseSchema):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
