from sqlalchemy.orm import Session

from ..models.history import UserHistory as HistoryModel
from ..schemas.history import HistoryCreate


def create_history(db: Session, history_in: HistoryCreate) -> HistoryModel:
    """Save a new user history record."""
    hist = HistoryModel(
        user_id=history_in.user_id,
        block_id=history_in.block_id,
        action=history_in.action,
    )
    db.add(hist)
    db.commit()
    db.refresh(hist)
    return hist


def list_history(
    db: Session, user_id: int | None = None, limit: int = 20
) -> list[HistoryModel]:
    """Return recent history records optionally filtered by user."""
    query = db.query(HistoryModel)
    if user_id:
        query = query.filter(HistoryModel.user_id == user_id)
    return query.order_by(HistoryModel.created_at.desc()).limit(limit).all()