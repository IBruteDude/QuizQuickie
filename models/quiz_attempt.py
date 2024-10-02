from sqlalchemy import Column, ForeignKey, Integer, Boolean
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class QuizAttempt(Base, BaseModel):
    """QuizAttempt DB model class"""

    __tablename__ = "quiz_attempt"

    def __init__(self, score, quiz_id, user_id, **kwargs):
        """initialize a QuizAttempt instance"""
        kwargs.update(score=score, quiz_id=quiz_id, user_id=user_id)
        super().__init__(**kwargs)

    score = Column(Integer, nullable=False)
    full_score = Column(Boolean, nullable=False)

    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    quiz = None
    user = None
    user_answers = relationship(
        "UserAnswer", back_populates="quiz_attempt", cascade="all, delete-orphan"
    )


from models.user_answer import UserAnswer

UserAnswer.quiz_attempt = relationship("QuizAttempt", back_populates="user_answers")
