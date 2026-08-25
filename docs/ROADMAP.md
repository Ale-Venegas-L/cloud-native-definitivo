# Classic Library delivery roadmap

## Hito 1 - Fundación segura e identidad

Status: in progress

- [x] Register the Firebase Web application in `colud-native`.
- [x] Add Google Sign-In configuration as code.
- [x] Introduce the `/api/v1` contract.
- [x] Add the modular FastAPI authentication boundary.
- [x] Protect all write operations with the admin role.
- [x] Add Vue session state, route guards and authenticated API client.
- [x] Add baseline authorization tests.
- [x] Deploy the Firebase Authentication provider configuration.
- [x] Assign the initial administrator claim to `vice.vasquez@duocuc.cl`.
- [ ] Complete a real browser login smoke test.

## Hito 1.5 - Experiencia de interfaz

Status: complete

- [x] Consolidate the editorial design system and responsive spacing.
- [x] Add responsive public and administrative navigation.
- [x] Add loading, error, empty and retry states.
- [x] Redesign the home, catalog, authentication and authorization views.
- [x] Add real covers, fallbacks, filters, sorting and book details.
- [x] Add a responsive operational dashboard and mobile CRUD cards.
- [x] Add destructive-action confirmation and complete content forms.
- [x] Add persistent light/dark theme controls and accessibility refinements.
- [x] Optimize and integrate the home hero as WebP.

## Hito 2 - Integridad del dominio

- Validate MongoDB identifiers without returning 500 errors.
- Enforce book-author relationships.
- Define author deletion policy.
- Disable in-memory database fallback outside tests and explicit local development.
- Add indexes, pagination and consistent error responses.

## Hito 3 - Calidad y delivery

- Add frontend component and route tests.
- Expand backend unit and integration coverage.
- Add linting, type checking and CI security gates.
- Produce production container images and health/readiness checks.

## Hito 4 - AWS API Gateway

- Select REST API plus Lambda Authorizer or HTTP API plus JWT Authorizer via ADR.
- Validate Firebase issuer, audience, signature and expiry at the edge.
- Add throttling, request validation, CORS, logs and metrics.
- Connect API Gateway to the private backend integration.
- Add WAF using the architecture selected in the ADR.
