from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.history import UserHistory, HistoryCreate
from ..services.history_logic import create_history, list_history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/", response_model=UserHistory)
def create_history_endpoint(
    payload: HistoryCreate, db: Session = Depends(get_db)
) -> UserHistory:
    return create_history(db, payload)


@router.get("/", response_model=list[UserHistory])
def list_history_endpoint(
    user_id: int | None = None, db: Session = Depends(get_db)
) -> list[UserHistory]:
    return list_history(db, user_id)