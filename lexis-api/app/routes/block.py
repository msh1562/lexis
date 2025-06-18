from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.block import Block, BlockCreate
from ..services.block_logic import (
    create_block,
    get_block,
    list_blocks,
    search_blocks,
)

router = APIRouter(prefix="/api/block", tags=["block"])


@router.post("/", response_model=Block)
def create_block_endpoint(
    payload: BlockCreate, db: Session = Depends(get_db)
) -> Block:
    """Create a new block."""
    return create_block(db, payload)


@router.get("/", response_model=list[Block])
def list_blocks_endpoint(
    topic: str | None = None,
    sort: str = "newest",
    db: Session = Depends(get_db),
) -> list[Block]:
    """Return all blocks filtered by topic and sorted."""
    return list_blocks(db, topic, sort)


@router.get("/search", response_model=list[Block])
def search_blocks_endpoint(q: str, db: Session = Depends(get_db)) -> list[Block]:
    """Search blocks by query string."""
    return search_blocks(db, q)


@router.get("/{block_id}", response_model=Block)
def read_block(block_id: int, db: Session = Depends(get_db)) -> Block:
    block = get_block(db, block_id)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    return block