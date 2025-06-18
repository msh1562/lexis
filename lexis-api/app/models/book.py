from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base
from .block import Block

class Book(Base):
    """Collection of blocks."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    blocks = relationship(
        Block,
        secondary="book_blocks",
        order_by="BookBlock.position",
    )

class BookBlock(Base):
    __tablename__ = "book_blocks"

    book_id = Column(Integer, ForeignKey("books.id"), primary_key=True)
    block_id = Column(Integer, ForeignKey("blocks.id"), primary_key=True)
    position = Column(Integer, nullable=False)