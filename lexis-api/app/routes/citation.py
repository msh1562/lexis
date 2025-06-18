from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.citation import CitationCreate, Citation, CitationGraph
from ..services.citation_logic import (
    create_citation,
    get_citation_graph,
    list_citations,
)

router = APIRouter(prefix="/api/citation", tags=["citation"])


@router.post("/", response_model=Citation)
def create_citation_endpoint(
    citation_in: CitationCreate, db: Session = Depends(get_db)
):
    try:
        return create_citation(db, citation_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[Citation])
def read_citations(
    from_block_id: int | None = None,
    to_block_id: int | None = None,
    db: Session = Depends(get_db),
):
    return list_citations(db, from_block_id, to_block_id)


@router.get("/graph/{block_id}", response_model=CitationGraph)
def read_citation_graph(block_id: int, db: Session = Depends(get_db)):
    data = get_citation_graph(db, block_id)
    if not data:
        raise HTTPException(status_code=404, detail="Block not found")
    return data