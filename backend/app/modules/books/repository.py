from typing import List, Optional
from bson import ObjectId
from app.core.database import get_database


def get_books() -> List[dict]:
    db = get_database()
    books = list(db.books.find())
    for book in books:
        book["id"] = str(book.pop("_id"))
    return books


def get_book_by_id(book_id: str) -> Optional[dict]:
    db = get_database()
    book = db.books.find_one({"_id": ObjectId(book_id)})
    if book:
        book["id"] = str(book.pop("_id"))
    return book


def create_book(book_data: dict) -> dict:
    db = get_database()
    result = db.books.insert_one(book_data)
    book_data["id"] = str(result.inserted_id)
    if "_id" in book_data:
        del book_data["_id"]
    return book_data


def update_book(book_id: str, book_data: dict) -> Optional[dict]:
    db = get_database()
    db.books.update_one({"_id": ObjectId(book_id)}, {"$set": book_data})
    return get_book_by_id(book_id)


def delete_book(book_id: str) -> bool:
    db = get_database()
    result = db.books.delete_one({"_id": ObjectId(book_id)})
    return result.deleted_count > 0


def get_books_by_author(author_id: str) -> List[dict]:
    db = get_database()
    books = list(db.books.find({"author_id": author_id}))
    for book in books:
        book["id"] = str(book.pop("_id"))
    return books
