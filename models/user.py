from sqlalchemy import Column, ForeignKey, String, VARBINARY, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base
from models.group_user import group_user


class User(Base, BaseModel):
    """User DB model class"""

    __tablename__ = "user"

    def __init__(
        self,
        email,
        password,
        user_name,
        first_name=None,
        last_name=None,
        reset_token=None,
        profile_picture=None,
        **kwargs
    ):
        """initialize a User instance"""
        kwargs.update(
            email=email,
            password=password,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            reset_token=reset_token,
            profile_picture=profile_picture,
        )
        super().__init__(**kwargs)

    email = Column(String(128), nullable=False, unique=True)
    password = Column(VARBINARY(60), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    user_name = Column(String(50), nullable=False, unique=True)
    reset_token = Column(Uuid, nullable=True)
    profile_picture = Column(String(256), nullable=True)

    groups = None
    quizs = relationship("Quiz", back_populates="user", cascade="all, delete-orphan")
    user_sessions = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )
    quiz_attempts = relationship(
        "QuizAttempt", back_populates="user", cascade="all, delete-orphan"
    )
    ownerships = relationship(
        "Ownership", back_populates="user", cascade="all, delete-orphan"
    )


from models.ownership import Ownership

Ownership.user = relationship("User", back_populates="ownerships")

from models.quiz import Quiz

Quiz.user = relationship("User", back_populates="quizs")

from models.quiz_attempt import QuizAttempt

QuizAttempt.user = relationship("User", back_populates="quiz_attempts")

from models.user_session import UserSession

UserSession.user = relationship("User", back_populates="user_sessions")
