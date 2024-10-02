from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base
from models.group_user import group_user


class Group(Base, BaseModel):
    """Group DB model class"""

    __tablename__ = "group"

    def __init__(self, title, ownership_id, **kwargs):
        """initialize a Group instance"""
        kwargs.update(title=title, ownership_id=ownership_id)
        super().__init__(**kwargs)

    title = Column(String(20), nullable=False)

    ownership_id = Column(Integer, ForeignKey("ownership.id"), nullable=False)

    ownership = None
    users = relationship(
        "User", viewonly=False, secondary=group_user, back_populates="groups"
    )
    quizs = relationship("Quiz", back_populates="group", cascade="all, delete-orphan")


from models.quiz import Quiz

Quiz.group = relationship("Group", back_populates="quizs")

from models.user import User

User.groups = relationship(
    "Group", viewonly=False, secondary=group_user, back_populates="users"
)
