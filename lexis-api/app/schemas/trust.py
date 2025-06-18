from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class VoteType(str, Enum):
    trust = "trust"
    distrust = "distrust"


class TrustVoteBase(BaseModel):
    block_id: int
    user_id: int
    vote: VoteType


class TrustVoteCreate(TrustVoteBase):
    pass


class TrustVote(TrustVoteBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TrustSummary(BaseModel):
    block_id: int
    trust: int
    distrust: int