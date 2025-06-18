from sqlalchemy.orm import Session

from ..models.topic import TopicNode
from ..schemas.topic import TopicNodeCreate


def create_topic(db: Session, node_in: TopicNodeCreate) -> TopicNode:
    parent = None
    depth = 0
    if node_in.parent_id is not None:
        parent = db.query(TopicNode).filter(TopicNode.id == node_in.parent_id).first()
        if not parent:
            raise ValueError("Parent not found")
        depth = parent.depth + 1
    node = TopicNode(name=node_in.name, parent_id=node_in.parent_id, depth=depth)
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


def list_topics(db: Session) -> list[TopicNode]:
    return db.query(TopicNode).order_by(TopicNode.depth, TopicNode.id).all()