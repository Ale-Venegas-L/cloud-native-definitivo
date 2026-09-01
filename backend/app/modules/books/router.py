from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.modules.books.schemas import BookCreate, BookUpdate, BookResponse
from app.modules.books import service
from app.modules.auth.dependencies import require_admin
from app.modules.auth.schemas import AuthenticatedUser

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/", response_model=List[BookResponse])
def get_books():
    return service.get_books()


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: str):
    book = service.get_book_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse, status_code=201)
def create_book(
    book: BookCreate,
    _: AuthenticatedUser = Depends(require_admin),
):
    return service.create_book(book)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: str,
    book: BookUpdate,
    _: AuthenticatedUser = Depends(require_admin),
):
    updated = service.update_book(book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: str,
    _: AuthenticatedUser = Depends(require_admin),
):
    deleted = service.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
