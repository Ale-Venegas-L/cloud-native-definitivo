from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author_id: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1, max_length=100)
    publication_year: int = Field(..., ge=1000, le=2100)
    genre: str = Field(..., min_length=1, max_length=100)
    description: str | None = None
    cover_url: str | None = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    author_id: str | None = Field(None, min_length=1)
    country: str | None = Field(None, min_length=1, max_length=100)
    publication_year: int | None = Field(None, ge=1000, le=2100)
    genre: str | None = Field(None, min_length=1, max_length=100)
    description: str | None = None
    cover_url: str | None = None


class BookResponse(BookBase):
    id: str

    model_config = {"from_attributes": True}
