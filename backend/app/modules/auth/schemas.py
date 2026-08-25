from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    uid: str
    email: str | None = None
    name: str | None = None
    picture: str | None = None
    admin: bool = False
    permissions: list[str] = Field(default_factory=list)
