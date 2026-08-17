from typing import List, Optional
from app.modules.authors import repository
from app.modules.authors.schemas import AuthorCreate, AuthorUpdate


def get_authors() -> List[dict]:
    return repository.get_authors()


def get_author_by_id(author_id: str) -> Optional[dict]:
    return repository.get_author_by_id(author_id)


def create_author(author: AuthorCreate) -> dict:
    author_data = author.model_dump()
    return repository.create_author(author_data)


def update_author(author_id: str, author: AuthorUpdate) -> Optional[dict]:
    author_data = author.model_dump(exclude_unset=True)
    return repository.update_author(author_id, author_data)


def delete_author(author_id: str) -> bool:
    return repository.delete_author(author_id)


def get_books_by_author(author_id: str) -> List[dict]:
    return repository.get_books_by_author(author_id)
