from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author_id: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1, max_length=100)
    publication_year: int = Field(..., ge=1000, le=2100)
    genre: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    cover_url: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author_id: Optional[str] = Field(None, min_length=1)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    publication_year: Optional[int] = Field(None, ge=1000, le=2100)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    cover_url: Optional[str] = None


class BookResponse(BookBase):
    id: str

    model_config = {"from_attributes": True}
