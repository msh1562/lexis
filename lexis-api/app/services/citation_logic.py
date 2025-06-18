from sqlalchemy.orm import Session

from sqlalchemy import or_

from ..models.citation import Citation as CitationModel, CitationType
from ..models.block import Block
from ..schemas.citation import (
    CitationCreate,
    CitationGraph,
    BlockNode,
    Citation,
)


def create_citation(db: Session, citation_in: CitationCreate) -> CitationModel:
    """Create a citation link between two blocks."""
    from_block = db.query(Block).filter(Block.id == citation_in.from_block_id).first()
    to_block = db.query(Block).filter(Block.id == citation_in.to_block_id).first()
    if not from_block or not to_block:
        raise ValueError("Invalid block ids")
    citation = CitationModel(
        from_block_id=citation_in.from_block_id,
        to_block_id=citation_in.to_block_id,
        type=citation_in.type,
        reason=citation_in.reason,
    )
    db.add(citation)
    db.commit()
    db.refresh(citation)
    return citation


def list_citations(
    db: Session,
    from_block_id: int | None = None,
    to_block_id: int | None = None,
) -> list[CitationModel]:
    """Retrieve citations optionally filtered by block."""
    query = db.query(CitationModel)
    if from_block_id is not None:
        query = query.filter(CitationModel.from_block_id == from_block_id)
    if to_block_id is not None:
        query = query.filter(CitationModel.to_block_id == to_block_id)
    return query.all()

def get_citation_graph(db: Session, block_id: int) -> CitationGraph | None:
    """Return connected blocks and citations for a given block."""
    block = db.query(Block).filter(Block.id == block_id).first()
    if not block:
        return None
    edges = (
        db.query(CitationModel)
        .filter(
            or_(
                CitationModel.from_block_id == block_id,
                CitationModel.to_block_id == block_id,
            )
        )
        .all()
    )
    node_ids = {block_id}
    for e in edges:
        node_ids.add(e.from_block_id)
        node_ids.add(e.to_block_id)
    nodes = db.query(Block).filter(Block.id.in_(node_ids)).all()
    node_objs = [BlockNode(id=n.id, title=n.title) for n in nodes]
    edge_objs = [
        Citation(
            id=e.id,
            from_block_id=e.from_block_id,
            to_block_id=e.to_block_id,
            type=e.type,
            reason=e.reason,
            created_at=e.created_at,
        )
        for e in edges
    ]
    return CitationGraph(blocks=node_objs, citations=edge_objs)