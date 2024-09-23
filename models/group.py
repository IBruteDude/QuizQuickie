from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base
from models.group_user import group_user


class Group(Base, BaseModel):
    """Group DB model class"""

    __tablename__ = "group"

    def __init__(self, *args, **kwargs):
        """initialize a Group instance"""
        super.__init__(*args, **kwargs)

    title = Column(String(20), nullable=False)

    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = None
    users = relationship("User", viewonly=False, secondary=group_user)
    quizs = relationship("Quiz", back_populates="group", cascade="all, delete-orphan")


from models.quiz import Quiz

Quiz.group = relationship("Group", back_populates="quizs")
from models.user import User

User.groups = relationship("Group", viewonly=False, secondary=group_user)
