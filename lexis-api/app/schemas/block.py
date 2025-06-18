from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from .citation import Citation

class BlockBase(BaseModel):
    title: str
    content: str
    topic: Optional[str] = None
    trust_score: float = 0.0
    source_url: Optional[str] = None


class BlockCreate(BlockBase):
    citation_ids: List[int] = []


class Block(BlockBase):
    id: int
    created_at: datetime
    citations: List[Citation] = []

    class Config:
        orm_mode = True