from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.trust import TrustVote, TrustVoteCreate, TrustSummary
from ..services.trust_logic import create_vote, get_vote_summary

router = APIRouter(prefix="/api/trust", tags=["trust"])


@router.post("/", response_model=TrustVote)
def create_vote_endpoint(payload: TrustVoteCreate, db: Session = Depends(get_db)) -> TrustVote:
    try:
        return create_vote(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{block_id}", response_model=TrustSummary)
def read_vote_summary(block_id: int, db: Session = Depends(get_db)) -> TrustSummary:
    return get_vote_summary(db, block_id)