from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, Enum as PgEnum, String, DateTime
from sqlalchemy.orm import relationship

from ..database import Base

class CitationType(Enum):
    """Kinds of citation relationships."""

    quote = "quote"
    refute = "refute"
    extend = "extend"


class Citation(Base):
    """Association representing one block citing another."""
    __tablename__ = "citations"

    id = Column(Integer, primary_key=True, index=True)
    from_block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    to_block_id = Column(Integer, ForeignKey("blocks.id"), nullable=False)
    type = Column(PgEnum(CitationType), nullable=False)
    # Optional explanation for the citation relationship
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    from_block = relationship(
        "Block",
        foreign_keys=[from_block_id],
        back_populates="citations",
    )
    to_block = relationship("Block", foreign_keys=[to_block_id])