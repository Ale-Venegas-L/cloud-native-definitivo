from fastapi import APIRouter, Depends

from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import AuthenticatedUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/me", response_model=AuthenticatedUser)
def get_me(
    user: AuthenticatedUser = Depends(get_current_user),
) -> AuthenticatedUser:
    return user
