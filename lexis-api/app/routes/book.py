from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.book import Book, BookCreate, BookUpdate
from ..services.book_logic import (
    create_book,
    get_book_by_slug,
    list_books,
    update_book,
    delete_book,
)

router = APIRouter(prefix="/api/book", tags=["book"])


@router.get("/", response_model=list[Book])
def list_books_endpoint(db: Session = Depends(get_db)) -> list[Book]:
    """Return all books."""
    return list_books(db)


@router.post("/", response_model=Book)
def create_book_endpoint(payload: BookCreate, db: Session = Depends(get_db)) -> Book:
    try:
        book = create_book(db, payload)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid block ids")
    return book


@router.get("/{slug}", response_model=Book)
def read_book(slug: str, db: Session = Depends(get_db)) -> Book:
    book = get_book_by_slug(db, slug)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{slug}", response_model=Book)
def update_book_endpoint(slug: str, payload: BookUpdate, db: Session = Depends(get_db)) -> Book:
    try:
        return update_book(db, slug, payload)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{slug}")
def delete_book_endpoint(slug: str, db: Session = Depends(get_db)) -> None:
    try:
        delete_book(db, slug)
    except ValueError:
        raise HTTPException(status_code=404, detail="Book not found")
    return None