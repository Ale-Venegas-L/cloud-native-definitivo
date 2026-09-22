from functools import lru_cache

import jwt
import requests
from jwt import PyJWKClient

from app.core.config import settings
from app.modules.auth.schemas import AuthenticatedUser

JWKS_URL = (
    f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/"
    f"{settings.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
)
ISSUER = (
    f"https://cognito-idp.{settings.COGNITO_REGION}.amazonaws.com/"
    f"{settings.COGNITO_USER_POOL_ID}"
)


@lru_cache(maxsize=1)
def _get_jwk_client() -> PyJWKClient:
    return PyJWKClient(JWKS_URL)


def verify_token(id_token: str) -> AuthenticatedUser:
    try:
        signing_key = _get_jwk_client().get_signing_key_from_jwt(id_token)
        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=settings.COGNITO_APP_CLIENT_ID,
            options={"require": ["exp", "iss", "aud", "sub"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token expired") from exc
    except (jwt.InvalidTokenError, jwt.InvalidAudienceError, jwt.InvalidIssuerError) as exc:
        raise ValueError(f"Invalid token: {exc}") from exc

    permissions: list[str] = claims.get("custom:permissions", [])
    if isinstance(permissions, str):
        permissions = [p.strip() for p in permissions.split(",") if p.strip()]

    return AuthenticatedUser(
        uid=claims["sub"],
        email=claims.get("email"),
        name=claims.get("name"),
        picture=claims.get("picture"),
        admin=str(claims.get("custom:admin", "")).lower() == "true",
        permissions=permissions,
    )
