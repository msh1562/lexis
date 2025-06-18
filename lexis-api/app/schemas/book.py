from datetime import datetime
from pydantic import BaseModel

from .block import Block

class BookCreate(BaseModel):
    title: str
    description: str | None = None
    block_ids: list[int]


class BookUpdate(BookCreate):
    pass


class Book(BaseModel):
    id: int
    slug: str
    title: str
    description: str | None = None
    created_at: datetime
    blocks: list[Block]

    class Config:
        orm_mode = True