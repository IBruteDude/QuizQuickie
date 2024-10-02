from sqlalchemy import Column, ForeignKey, BOOLEAN, Integer, String
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Answer(Base, BaseModel):
    """Answer DB model class"""

    __tablename__ = "answer"

    def __init__(self, text, order, question_id, correct, **kwargs):
        """initialize a Answer instance"""
        kwargs.update(text=text, order=order, question_id=question_id, correct=correct)
        super().__init__(**kwargs)

    text = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    correct = Column(BOOLEAN, nullable=False)

    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    question = None
