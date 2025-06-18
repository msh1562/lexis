from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as PgEnum
from sqlalchemy.orm import relationship

from ..database import Base

class HistoryAction(Enum):
    view = "view"
    like = "like"
    bookmark = "bookmark"

class UserHistory(Base):
    """Record of user interactions with blocks."""

    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    action = Column(PgEnum(HistoryAction), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    block = relationship("Block")