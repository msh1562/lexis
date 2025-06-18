from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.orm import relationship

from ..database import Base

class Block(Base):
    """Content block."""
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    # Optional topic for categorizing blocks. Nullable for unclassified content.
    topic = Column(String, nullable=True, index=True)
    # URL of the original source when imported from TraceFact
    source_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    trust_score = Column(Float, default=0.0)

    # blocks this block cites
    citations = relationship(
        "Citation",
        foreign_keys="Citation.from_block_id",
        back_populates="from_block",
        cascade="all, delete-orphan",
    )