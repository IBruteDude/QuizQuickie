from sqlalchemy import Table, Column, ForeignKey, Integer
from models.base import Base

user_quiz_attempt = Table(
    "user_quiz_attempt",
    Base.metadata,
    Column(
        "attempt_id",
        Integer,
        ForeignKey("quiz_attempt.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        Integer,
        ForeignKey("user.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    ),
)
