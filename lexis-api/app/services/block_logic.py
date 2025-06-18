from sqlalchemy.orm import Session
from sqlalchemy import or_

from ..models.block import Block
from ..models.citation import Citation, CitationType
from ..schemas.block import BlockCreate


def create_block(db: Session, block_in: BlockCreate) -> Block:
    """Persist a new block to the database."""
    block = Block(
        title=block_in.title,
        content=block_in.content,
        topic=block_in.topic,
        trust_score=block_in.trust_score,
        source_url=block_in.source_url,
    )
    db.add(block)
    db.flush()
    for cited_id in block_in.citation_ids:
        db.add(
            Citation(
                from_block_id=block.id,
                to_block_id=cited_id,
                type=CitationType.quote,
            )
        )
    db.commit()
    db.refresh(block)
    return block


def get_block(db: Session, block_id: int) -> Block | None:
    """Retrieve a block by ID."""
    return db.query(Block).filter(Block.id == block_id).first()


def list_blocks(
    db: Session, topic: str | None = None, sort: str = "newest"
) -> list[Block]:
    """Return blocks optionally filtered by topic and sorted."""

    query = db.query(Block)
    if topic:
        query = query.filter(Block.topic == topic)

    if sort == "oldest":
        query = query.order_by(Block.created_at.asc())
    elif sort == "trust":
        query = query.order_by(Block.trust_score.desc())
    else:  # newest
        query = query.order_by(Block.created_at.desc())

    return query.all()


def search_blocks(db: Session, query: str) -> list[Block]:
    """Search blocks by title or content substring."""
    pattern = f"%{query}%"
    return (
        db.query(Block)
        .filter(or_(Block.title.ilike(pattern), Block.content.ilike(pattern)))
        .order_by(Block.created_at.desc())
        .all()
    )