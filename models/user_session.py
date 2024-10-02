from sqlalchemy import Column, ForeignKey, DATETIME, Integer, Uuid
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class UserSession(Base, BaseModel):
    """UserSession DB model class"""

    __tablename__ = "user_session"

    def __init__(self, expiry_date, uuid, user_id, **kwargs):
        """initialize a UserSession instance"""
        kwargs.update(expiry_date=expiry_date, uuid=uuid, user_id=user_id)
        super().__init__(**kwargs)

    expiry_date = Column(DATETIME, nullable=False)
    uuid = Column(Uuid, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = None
