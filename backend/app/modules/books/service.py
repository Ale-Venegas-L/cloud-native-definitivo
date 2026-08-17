from typing import List, Optional
from app.modules.books import repository
from app.modules.books.schemas import BookCreate, BookUpdate


def get_books() -> List[dict]:
    return repository.get_books()


def get_book_by_id(book_id: str) -> Optional[dict]:
    return repository.get_book_by_id(book_id)


def create_book(book: BookCreate) -> dict:
    book_data = book.model_dump()
    return repository.create_book(book_data)


def update_book(book_id: str, book: BookUpdate) -> Optional[dict]:
    book_data = book.model_dump(exclude_unset=True)
    return repository.update_book(book_id, book_data)


def delete_book(book_id: str) -> bool:
    return repository.delete_book(book_id)


def get_books_by_author(author_id: str) -> List[dict]:
    return repository.get_books_by_author(author_id)
