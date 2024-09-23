from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base
from models.user_quiz_attempt import user_quiz_attempt


class QuizAttempt(Base, BaseModel):
    """QuizAttempt DB model class"""

    __tablename__ = "quiz_attempt"

    def __init__(self, *args, **kwargs):
        """initialize a QuizAttempt instance"""
        super.__init__(*args, **kwargs)

    score = Column(Integer, nullable=False)

    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)

    users = None
    quiz = None
    user_answers = relationship(
        "UserAnswer", back_populates="quiz_attempt", cascade="all, delete-orphan"
    )


from models.user_answer import UserAnswer

UserAnswer.quiz_attempt = relationship("QuizAttempt", back_populates="user_answers")
