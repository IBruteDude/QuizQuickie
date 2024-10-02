from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Question(Base, BaseModel):
    """Question DB model class"""

    __tablename__ = "question"

    def __init__(self, statement, quiz_id, points, type, order, **kwargs):
        """initialize a Question instance"""
        kwargs.update(
            statement=statement, quiz_id=quiz_id, points=points, type=type, order=order
        )
        super().__init__(**kwargs)

    statement = Column(String(200), nullable=False)
    points = Column(Integer, nullable=False)
    type = Column(String(3), nullable=False)
    order = Column(Integer, nullable=False)

    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)

    quiz = None
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
    user_answers = relationship(
        "UserAnswer", back_populates="question", cascade="all, delete-orphan"
    )


from models.answer import Answer

Answer.question = relationship("Question", back_populates="answers")

from models.user_answer import UserAnswer

UserAnswer.question = relationship("Question", back_populates="user_answers")
