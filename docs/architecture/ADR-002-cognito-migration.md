# ADR-002: Migración de Firebase Authentication a AWS Cognito

- Status: accepted
- Date: 2026-09-08

## Context

Classic Library initially used Firebase Authentication with Google Sign-In as the identity provider (ADR-001). The project requirements for Prueba 1 mandate:

- AWS API Gateway as the API management layer
- AWS Cognito as the IDaaS tenant
- OAuth 2.0 / OpenID Connect with Authorization Code + PKCE flow
- JWT validation at the API Gateway level
- IAM roles for access control

Firebase Authentication does not integrate with AWS API Gateway's JWT authorizer and does not support the PKCE flow required by the evaluation criteria. Migrating to Cognito aligns the identity provider with the AWS ecosystem and satisfies all Prueba 1 requirements.

## Decision

- Replace Firebase Authentication with Amazon Cognito User Pool as the external identity provider.
- The Vue application uses the Cognito Hosted UI with OAuth 2.0 Authorization Code + PKCE flow.
- Cognito issues JWTs with custom claims (`custom:admin`, `custom:permissions`) via a Pre Token Generation Lambda trigger.
- FastAPI validates Cognito JWTs by verifying the signature against the JWKS endpoint, validating issuer and audience.
- AWS API Gateway sits in front of the backend, applying JWT validation on protected routes (POST, PUT, DELETE).
- IAM roles control API Gateway's ability to invoke the backend.
- The backend remains a local Docker Compose deployment during development; API Gateway points to the local backend via a public endpoint or VPN.

## Consequences

### Positive
- Native integration with AWS API Gateway JWT authorizer
- OIDC-compliant PKCE flow satisfies Prueba 1 requirements
- Centralized user management in AWS Console
- Custom claims (admin, permissions) embedded in JWT via Lambda trigger
- No dependency on Google Firebase SDK in frontend or backend

### Negative
- Migration required changes across 12+ files (backend, frontend, docs)
- Custom attributes must be defined at User Pool creation time
- Pre Token Generation Lambda adds operational complexity
- No built-in refresh token rotation (must be implemented if needed)

### Neutral
- The `AuthenticatedUser` schema remains unchanged (provider-agnostic)
- The `api.ts` service layer is simplified (no token refresh retry logic)
- Route guards in the router remain functionally identical
- The `set_admin.py` script now uses boto3 instead of Firebase Admin SDK

## Migration scope

| Component | Before | After |
|---|---|---|
| Identity provider | Firebase Authentication | Amazon Cognito |
| Frontend auth SDK | `firebase` npm package | Pure PKCE (no SDK) |
| Backend token verification | `firebase-admin` SDK | `PyJWT` + JWKS |
| API management | Direct FastAPI access | AWS API Gateway |
| Custom claims | Firebase custom claims | Cognito custom attributes + Lambda |
| Login flow | Google Sign-In popup | Cognito Hosted UI redirect |
| Admin management | `firebase-admin` set_custom_user_claims | `boto3` admin_update_user_attrs |

## References

- [AWS Cognito Documentation](https://docs.aws.amazon.com/cognito/)
- [API Gateway JWT Authorizer](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html)
- [OAuth 2.0 PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- `docs/aws-setup.md` — Step-by-step AWS configuration guide
