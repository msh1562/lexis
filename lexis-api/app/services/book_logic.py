from typing import List
from sqlalchemy.orm import Session

from ..models.book import Book, BookBlock
from ..models.block import Block
from ..schemas.book import BookCreate, BookUpdate


def slugify(title: str) -> str:
    return (
        title.lower()
        .strip()
        .replace(" ", "-")
        .replace("/", "-")
    )


def create_book(db: Session, book_in: BookCreate) -> Book:
    blocks = (
        db.query(Block).filter(Block.id.in_(book_in.block_ids)).order_by(Block.id).all()
    )
    if len(blocks) != len(book_in.block_ids):
        raise ValueError("Invalid block ids")

    slug_base = slugify(book_in.title)
    slug = slug_base
    idx = 1
    while db.query(Book).filter(Book.slug == slug).first():
        idx += 1
        slug = f"{slug_base}-{idx}"

    book = Book(title=book_in.title, description=book_in.description, slug=slug)
    db.add(book)
    db.flush()  # assign id

    for pos, block_id in enumerate(book_in.block_ids):
        db.add(BookBlock(book_id=book.id, block_id=block_id, position=pos))

    db.commit()
    return db.query(Book).filter(Book.id == book.id).first()


def get_book_by_slug(db: Session, slug: str) -> Book | None:
    return db.query(Book).filter(Book.slug == slug).first()


def list_books(db: Session) -> List[Book]:
    """Return all books ordered by creation id."""
    return db.query(Book).order_by(Book.id).all()


def update_book(db: Session, slug: str, book_in: BookUpdate) -> Book:
    book = get_book_by_slug(db, slug)
    if not book:
        raise ValueError("Book not found")

    book.title = book_in.title
    book.description = book_in.description
    db.query(BookBlock).filter(BookBlock.book_id == book.id).delete()
    for pos, block_id in enumerate(book_in.block_ids):
        db.add(BookBlock(book_id=book.id, block_id=block_id, position=pos))
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, slug: str) -> None:
    book = get_book_by_slug(db, slug)
    if not book:
        raise ValueError("Book not found")
    db.query(BookBlock).filter(BookBlock.book_id == book.id).delete()
    db.delete(book)
    db.commit()