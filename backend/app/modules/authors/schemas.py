from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    country: str = Field(..., min_length=1, max_length=100)
    birth_year: int = Field(..., ge=1000, le=2100)
    death_year: int | None = Field(None, ge=1000, le=2100)
    biography: str | None = None
    image_url: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    country: str | None = Field(None, min_length=1, max_length=100)
    birth_year: int | None = Field(None, ge=1000, le=2100)
    death_year: int | None = Field(None, ge=1000, le=2100)
    biography: str | None = None
    image_url: str | None = None


class AuthorResponse(AuthorBase):
    id: str

    model_config = {"from_attributes": True}
