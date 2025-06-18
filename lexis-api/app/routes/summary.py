from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.summary import SummaryRequest, SummaryResponse
from ..schemas.block import Block, BlockCreate
from ..services.summary_logic import summarize_text
from ..services.block_logic import create_block
from ..database import get_db

router = APIRouter(prefix="/api/lexify", tags=["lexify"])

@router.post("/summary", response_model=SummaryResponse)
def lexify_summary(payload: SummaryRequest) -> SummaryResponse:
    """Return summarized text."""
    summary_text = summarize_text(payload.text)
    return SummaryResponse(summary=summary_text)


@router.post("/fromTraceFact", response_model=Block)
def create_from_trace_fact(
    payload: BlockCreate, db: Session = Depends(get_db)
) -> Block:
    """Create a block from TraceFact data."""
    return create_block(db, payload)