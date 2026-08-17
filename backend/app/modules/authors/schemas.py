from pydantic import BaseModel, Field
from typing import Optional


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    country: str = Field(..., min_length=1, max_length=100)
    birth_year: int = Field(..., ge=1000, le=2100)
    death_year: Optional[int] = Field(None, ge=1000, le=2100)
    biography: Optional[str] = None
    image_url: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    birth_year: Optional[int] = Field(None, ge=1000, le=2100)
    death_year: Optional[int] = Field(None, ge=1000, le=2100)
    biography: Optional[str] = None
    image_url: Optional[str] = None


class AuthorResponse(AuthorBase):
    id: str

    model_config = {"from_attributes": True}
