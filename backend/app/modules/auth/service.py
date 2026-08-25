from functools import lru_cache
from typing import Any

import firebase_admin
from firebase_admin import auth as firebase_auth

from app.core.config import settings
from app.modules.auth.schemas import AuthenticatedUser


@lru_cache(maxsize=1)
def initialize_firebase() -> firebase_admin.App:
    """Initialize the Admin SDK once using workload credentials when available."""
    try:
        return firebase_admin.get_app()
    except ValueError:
        return firebase_admin.initialize_app(
            options={"projectId": settings.FIREBASE_PROJECT_ID}
        )


def verify_token(id_token: str) -> AuthenticatedUser:
    if id_token.count(".") != 2:
        raise ValueError("Malformed Firebase ID token")

    app = initialize_firebase()
    claims: dict[str, Any] = firebase_auth.verify_id_token(
        id_token,
        app=app,
        check_revoked=settings.FIREBASE_CHECK_REVOKED,
    )

    permissions = claims.get("permissions", [])
    if not isinstance(permissions, list):
        permissions = []

    return AuthenticatedUser(
        uid=claims["uid"],
        email=claims.get("email"),
        name=claims.get("name"),
        picture=claims.get("picture"),
        admin=claims.get("admin") is True,
        permissions=[str(permission) for permission in permissions],
    )
