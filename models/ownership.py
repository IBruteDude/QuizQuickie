from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base import BaseModel, Base


class Ownership(Base, BaseModel):
    """Ownership DB model class"""

    __tablename__ = "ownership"

    def __init__(self, user_id, **kwargs):
        """initialize a Ownership instance"""
        kwargs.update(user_id=user_id)
        super().__init__(**kwargs)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    groups = relationship(
        "Group", back_populates="ownership", cascade="all, delete-orphan"
    )
    user = None


from models.group import Group

Group.ownership = relationship("Ownership", back_populates="groups")
