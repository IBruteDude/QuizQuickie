from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class UserAnswer(Base, BaseModel):
    """UserAnswer DB model class"""

    __tablename__ = "user_answer"

    def __init__(self, *args, **kwargs):
        """initialize a UserAnswer instance"""
        super.__init__(*args, **kwargs)

    answer = Column(Integer, nullable=False)

    attempt_id = Column(Integer, ForeignKey("quiz_attempt.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    quiz_attempt = None
    question = None
