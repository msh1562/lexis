from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base

class TopicNode(Base):
    """Topic tree node."""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    depth = Column(Integer, nullable=False, default=0)

    parent = relationship("TopicNode", remote_side=[id], back_populates="children")
    children = relationship(
        "TopicNode",
        back_populates="parent",
        cascade="all, delete-orphan",
        single_parent=True,
    )
