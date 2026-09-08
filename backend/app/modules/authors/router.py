from fastapi import APIRouter, Depends, HTTPException

from app.modules.auth.dependencies import require_admin
from app.modules.auth.schemas import AuthenticatedUser
from app.modules.authors import service
from app.modules.authors.schemas import AuthorCreate, AuthorResponse, AuthorUpdate
from app.modules.books.schemas import BookResponse

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/", response_model=list[AuthorResponse])
def get_authors():
    return service.get_authors()


@router.get("/{author_id}", response_model=AuthorResponse)
def get_author(author_id: str):
    author = service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=AuthorResponse, status_code=201)
def create_author(
    author: AuthorCreate,
    _: AuthenticatedUser = Depends(require_admin),
):
    return service.create_author(author)


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author(
    author_id: str,
    author: AuthorUpdate,
    _: AuthenticatedUser = Depends(require_admin),
):
    updated = service.update_author(author_id, author)
    if not updated:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated


@router.delete("/{author_id}", status_code=204)
def delete_author(
    author_id: str,
    _: AuthenticatedUser = Depends(require_admin),
):
    deleted = service.delete_author(author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Author not found")


@router.get("/{author_id}/books", response_model=list[BookResponse])
def get_author_books(author_id: str):
    author = service.get_author_by_id(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return service.get_books_by_author(author_id)
