from typing import Optional
from pydantic import BaseModel

class TopicNodeBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class TopicNodeCreate(TopicNodeBase):
    pass

class TopicNode(TopicNodeBase):
    id: int
    depth: int

    class Config:
        orm_mode = True