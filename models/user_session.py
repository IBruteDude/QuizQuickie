from sqlalchemy import Column, ForeignKey, Uuid, Integer, DATETIME
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class UserSession(Base, BaseModel):
    """UserSession DB model class"""

    __tablename__ = "user_session"

    def __init__(self, *args, **kwargs):
        """initialize a UserSession instance"""
        super.__init__(*args, **kwargs)

    expiry_date = Column(DATETIME, nullable=False)
    uuid = Column(Uuid, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = None
