from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class CitationType(str, Enum):
    quote = "quote"
    refute = "refute"
    extend = "extend"

class CitationBase(BaseModel):
    from_block_id: int
    to_block_id: int
    type: CitationType
    reason: str | None = None


class CitationCreate(CitationBase):
    pass

class Citation(CitationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class BlockNode(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CitationGraph(BaseModel):
    """Graph of blocks and citation edges"""

    blocks: list[BlockNode]
    citations: list[Citation]

    class Config:
        orm_mode = True