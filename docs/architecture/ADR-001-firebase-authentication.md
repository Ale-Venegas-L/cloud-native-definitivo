# ADR-001: Firebase Authentication for the modular monolith

- Status: accepted
- Date: 2026-08-24

## Context

Classic Library is a Vue 3 and FastAPI modular monolith. The course material uses
Microsoft Entra ID, MSAL, Spring Security and AWS API Gateway to demonstrate an
OIDC/OAuth2 architecture. This project uses Firebase Authentication with Google
Sign-In while preserving the same trust boundaries.

## Decision

- Firebase Authentication is the external identity provider.
- The Vue application obtains a Firebase ID token and sends it as a bearer token.
- FastAPI acts as the resource server and validates every protected request.
- Public reads remain anonymous; all mutations require the `admin: true` claim.
- Route guards improve UX but never replace backend authorization.
- Firebase Admin credentials are supplied by the runtime and never committed.
- Administrator claims are granted only through the privileged
  `backend/scripts/set_admin.py` command after the user's first Google login.
- AWS API Gateway will be introduced as a later milestone without changing the
  domain modules or the public API contract.

## Consequences

- Authentication concerns remain isolated in `app.modules.auth`.
- `books` and `authors` only depend on authorization dependencies, not Firebase.
- The API uses `/api/v1` now so the future Gateway can expose a stable contract.
- Firebase ID tokens differ from Entra access tokens with custom API scopes. The
  project uses signed custom claims for authorization and records this adaptation.
