from sqlalchemy import Column, ForeignKey, DATETIME, Integer, String
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Quiz(Base, BaseModel):
    """Quiz DB model class"""

    __tablename__ = "quiz"

    def __init__(
        self,
        title,
        category,
        difficulty,
        points,
        user_id,
        group_id=None,
        duration=None,
        start=None,
        end=None,
        **kwargs
    ):
        """initialize a Quiz instance"""
        kwargs.update(
            title=title,
            category=category,
            difficulty=difficulty,
            points=points,
            user_id=user_id,
            group_id=group_id,
            duration=duration,
            start=start,
            end=end,
        )
        super().__init__(**kwargs)

    title = Column(String(50), nullable=False)
    category = Column(String(20), nullable=False)
    difficulty = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=True)
    start = Column(DATETIME, nullable=True)
    end = Column(DATETIME, nullable=True)

    group_id = Column(Integer, ForeignKey("group.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    group = None
    user = None
    questions = relationship(
        "Question", back_populates="quiz", cascade="all, delete-orphan"
    )
    quiz_attempts = relationship(
        "QuizAttempt", back_populates="quiz", cascade="all, delete-orphan"
    )


from models.question import Question

Question.quiz = relationship("Quiz", back_populates="questions")

from models.quiz_attempt import QuizAttempt

QuizAttempt.quiz = relationship("Quiz", back_populates="quiz_attempts")
