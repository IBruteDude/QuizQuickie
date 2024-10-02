from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class UserAnswer(Base, BaseModel):
    """UserAnswer DB model class"""

    __tablename__ = "user_answer"

    def __init__(self, attempt_id, answer, question_id, **kwargs):
        """initialize a UserAnswer instance"""
        kwargs.update(attempt_id=attempt_id, answer=answer, question_id=question_id)
        super().__init__(**kwargs)

    answer = Column(Integer, nullable=False)

    attempt_id = Column(Integer, ForeignKey("quiz_attempt.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    quiz_attempt = None
    question = None
