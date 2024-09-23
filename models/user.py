from sqlalchemy import Column, ForeignKey, String, VARBINARY
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base
from models.group_user import group_user
from models.user_quiz_attempt import user_quiz_attempt


class User(Base, BaseModel):
    """User DB model class"""

    __tablename__ = "user"

    def __init__(self, *args, **kwargs):
        """initialize a User instance"""
        super.__init__(*args, **kwargs)

    email = Column(String(128), nullable=False, unique=True)
    password = Column(VARBINARY(60), nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    user_name = Column(String(50), nullable=False, unique=True)
    reset_token = Column(String(8), nullable=True)
    profile_picture_url = Column(String(256), nullable=True)

    groups = relationship("Group", back_populates="user", cascade="all, delete-orphan")
    groups = None
    user_sessions = relationship(
        "UserSession", back_populates="user", cascade="all, delete-orphan"
    )
    quiz_attempts = relationship(
        "QuizAttempt", viewonly=False, secondary=user_quiz_attempt
    )


from models.group import Group

Group.user = relationship("User", back_populates="groups")
from models.quiz_attempt import QuizAttempt

QuizAttempt.users = relationship("User", viewonly=False, secondary=user_quiz_attempt)
from models.user_session import UserSession

UserSession.user = relationship("User", back_populates="user_sessions")
