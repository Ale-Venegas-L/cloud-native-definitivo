from bson import ObjectId

from app.core.database import get_database


def get_authors() -> list[dict]:
    db = get_database()
    authors = list(db.authors.find())
    for author in authors:
        author["id"] = str(author.pop("_id"))
    return authors


def get_author_by_id(author_id: str) -> dict | None:
    db = get_database()
    author = db.authors.find_one({"_id": ObjectId(author_id)})
    if author:
        author["id"] = str(author.pop("_id"))
    return author


def create_author(author_data: dict) -> dict:
    db = get_database()
    result = db.authors.insert_one(author_data)
    author_data["id"] = str(result.inserted_id)
    if "_id" in author_data:
        del author_data["_id"]
    return author_data


def update_author(author_id: str, author_data: dict) -> dict | None:
    db = get_database()
    db.authors.update_one({"_id": ObjectId(author_id)}, {"$set": author_data})
    return get_author_by_id(author_id)


def delete_author(author_id: str) -> bool:
    db = get_database()
    result = db.authors.delete_one({"_id": ObjectId(author_id)})
    return result.deleted_count > 0


def get_books_by_author(author_id: str) -> list[dict]:
    db = get_database()
    books = list(db.books.find({"author_id": author_id}))
    for book in books:
        book["id"] = str(book.pop("_id"))
    return books
