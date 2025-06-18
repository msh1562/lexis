from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class HistoryAction(str, Enum):
    view = "view"
    like = "like"
    bookmark = "bookmark"

class HistoryBase(BaseModel):
    user_id: int
    block_id: int
    action: HistoryAction

class HistoryCreate(HistoryBase):
    pass

class UserHistory(HistoryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True