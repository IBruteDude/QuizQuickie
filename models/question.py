from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Question(Base, BaseModel):
    """Question DB model class"""

    __tablename__ = "question"

    def __init__(self, *args, **kwargs):
        """initialize a Question instance"""
        super.__init__(*args, **kwargs)

    statement = Column(String(200), nullable=False)
    points = Column(Integer, nullable=False)
    type = Column(String(3), nullable=False)

    quiz_id = Column(Integer, ForeignKey("quiz.id"), nullable=False)

    quiz = None
    answers = relationship(
        "Answer", back_populates="question", cascade="all, delete-orphan"
    )
    user_answers = relationship(
        "UserAnswer", back_populates="question", cascade="all, delete-orphan"
    )


from models.user_answer import UserAnswer

UserAnswer.question = relationship("Question", back_populates="user_answers")
from models.answer import Answer

Answer.question = relationship("Question", back_populates="answers")
