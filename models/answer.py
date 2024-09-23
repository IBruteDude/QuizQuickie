from sqlalchemy import Column, ForeignKey, String, Integer, BOOLEAN
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Answer(Base, BaseModel):
    """Answer DB model class"""

    __tablename__ = "answer"

    def __init__(self, *args, **kwargs):
        """initialize a Answer instance"""
        super.__init__(*args, **kwargs)

    text = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    correct = Column(BOOLEAN, nullable=False)

    question_id = Column(Integer, ForeignKey("question.id"), nullable=False)

    question = None
