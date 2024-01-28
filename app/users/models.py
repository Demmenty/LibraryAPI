from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer,
                        LargeBinary, String, func)
from sqlalchemy.orm import relationship

from app.auth.models import Base
from app.users.schemas import MembershipStatus, UserRole


class LibraryMemberModel(Base):
    """ Модель члена библиотеки в базе данных """

    __tablename__ = "library_member"

    id = Column(Integer, primary_key=True, index=True)
    contact_information = Column(String)
    membership_status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE)
    membership_period = Column(DateTime, default=func.now())

    user = relationship("UserModel", back_populates="library_member")

    def __str__(self):
        return f" Library member {self.id}"


class UserModel(Base):
    """ Модель пользователя в базе данных """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(LargeBinary)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    library_member_id = Column(Integer, ForeignKey("library_member.id", ondelete="CASCADE"), nullable=True)

    library_member = relationship("LibraryMemberModel", back_populates="user")
    refresh_tokens = relationship("RefreshTokenModel", back_populates="user")

    def __str__(self):
        return f" User {self.username}"
