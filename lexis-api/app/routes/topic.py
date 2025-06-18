from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.topic import TopicNode, TopicNodeCreate
from ..services.topic_logic import create_topic, list_topics

router = APIRouter(prefix="/api/topic", tags=["topic"])


@router.post("/", response_model=TopicNode)
def create_topic_endpoint(payload: TopicNodeCreate, db: Session = Depends(get_db)) -> TopicNode:
    try:
        return create_topic(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[TopicNode])
def list_topics_endpoint(db: Session = Depends(get_db)) -> list[TopicNode]:
    return list_topics(db)