from sqlalchemy import Table, Column, ForeignKey, Integer
from models.base import Base

group_user = Table(
    "group_user",
    Base.metadata,
    Column(
        "group_id",
        Integer,
        ForeignKey("group.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)
