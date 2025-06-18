from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum as PgEnum
from sqlalchemy.orm import relationship

from ..database import Base


class VoteType(Enum):
    """Possible trust vote options."""

    trust = "trust"
    distrust = "distrust"


class TrustVote(Base):
    """User vote indicating trust or distrust in a block."""

    __tablename__ = "trust_votes"

    id = Column(Integer, primary_key=True, index=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vote = Column(PgEnum(VoteType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    block = relationship("Block")
    user = relationship("User")