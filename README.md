# Classic Library

Biblioteca web de literatura clásica. MVP full-stack desarrollado como proyecto académico.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | Vue 3.5, TypeScript 6, Vite 8, Tailwind CSS 4 |
| Backend | Python 3.14, FastAPI, Pydantic, PyMongo |
| Base de datos | MongoDB 7 |
| Autenticación | AWS Cognito (OAuth 2.0 PKCE) |
| API Gateway | AWS API Gateway REST |
| Contenedores | Docker, Docker Compose |

## Arquitectura

```text
Frontend (Vue 3)
   │
   │ OAuth 2.0 / PKCE
   v
AWS Cognito (User Pool)
   │
   │ JWT
   v
AWS API Gateway
   │
   │ IAM + JWT Authorizer
   v
FastAPI REST API (/api/v1) → MongoDB
```

Módulos del backend: `auth`, `books`, `authors`. Cada módulo sigue el patrón router → service → repository.

## Requisitos — Prueba 1

### Criterios de evaluación

1. Creación de instancia de API Manager en funcionamiento en la plataforma cloud.
2. Configuración del API Manager para llamar a los endpoints del backend.
3. Frontend consume endpoints a través del API Manager correctamente configurado.
4. API Manager valida JWT: rechaza peticiones inválidas, acepta las correctas.
5. Creación del tenant en IDaaS con usuarios registrados.
6. Frontend utiliza OAuth 2.0/OpenID Connect para iniciar sesión y obtener JWT válido.
7. Backend y frontend desplegados, activos e integrados en la nube.

### Indicadores de evaluación

| Indicador | Descripción |
|---|---|
| Rutas API Manager | Todas las rutas creadas y dirigidas a los microservicios correspondientes |
| CORS API Manager | Configurado de forma segura, orígenes permitidos definidos correctamente |
| Tenant IDaaS | Tenant creado con usuarios de prueba, roles, políticas y parámetros |
| Aplicación IDaaS | Registrada con clientId, URIs de redirección, roles y scopes |
| Flujo usuario | Registro e inicio de sesión funcional, tokens con claims esperados |
| OIDC PKCE | Authorization Code con PKCE: code verifier, code challenge, state, nonce |
| Validación JWT API Manager | Todas las rutas aplican validación JWT, verifica issuer y audience |
| Evidencia de rutas | Llamadas con y sin token, respuestas 200/401/403 coherentes |

Ver `docs/aws-setup.md` para la guía paso a paso de configuración en AWS.

## Estado actual

### Implementado

| Componente | Estado |
|---|---|
| Frontend Vue 3 | Completo — catálogo público, admin CRUD, auth Cognito PKCE |
| Backend FastAPI | Completo — módulos auth/books/authors, CORS, health |
| MongoDB | Completo — conexión, seed data, mongomock fallback |
| Cognito JWT verification | Completo — JWKS, issuer/audience validation, custom claims |
| Docker Compose | Completo — 3 servicios (mongodb, backend, frontend) |
| Tests backend | Completos — pytest + coverage |
| Tests frontend | Completos — Vitest + Vue Test Utils |

### Pendiente (Prueba 1)

| Componente | Estado |
|---|---|
| AWS API Gateway | Configuración manual pendiente (ver `docs/aws-setup.md`) |
| Cognito User Pool | Configuración manual pendiente (ver `docs/aws-setup.md`) |
| Despliegue cloud | No implementado — solo ejecución local vía docker-compose |
| CI/CD | No configurado — `.github/workflows/` vacío |
| WAF | No implementado |

### Roadmap

Ver `docs/ROADMAP.md` para el detalle de hitos.

| Hito | Descripción | Estado |
|---|---|---|
| Hito 1 | Fundación segura e identidad | En progreso |
| Hito 1.5 | Experiencia de interfaz | Completo |
| Hito 2 | Integridad del dominio | Planificado |
| Hito 3 | Calidad y delivery | Planificado |
| Hito 4 | AWS API Gateway | En progreso |

## Decisiones de arquitectura

- `docs/architecture/ADR-001-firebase-authentication.md` — Decisión original (Firebase)
- `docs/architecture/ADR-002-cognito-migration.md` — Migración a Cognito

## Estructura del proyecto

```text
MVP-AWS-DESARROLLO-CLOUD-NATIVE-I_004D-/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py             # Entry point, CORS, lifespan
│   │   ├── core/               # Config, database
│   │   ├── modules/            # auth, books, authors
│   │   └── shared/             # Seed data
│   ├── scripts/                # set_admin.py
│   ├── tests/                  # pytest
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                   # Vue 3 SPA
│   ├── src/
│   │   ├── composables/        # useAuth, useTheme, useScrollReveal
│   │   ├── components/         # Pages, UI, views, modals
│   │   ├── services/           # api.ts (HTTP client)
│   │   ├── router/             # Rutas + guards
│   │   ├── lib/                # cognito.ts
│   │   └── types/              # domain.ts
│   ├── Dockerfile
│   └── package.json
│
├── docs/
│   ├── ROADMAP.md
│   ├── aws-setup.md            # Guía configuración AWS
│   └── architecture/
├── design/                     # Assets de diseño
├── docker-compose.yml
└── .env.example
```

## Arranque rápido

### Requisitos

- Git, Python 3.14+, Node.js 22+, Docker Desktop
- AWS Console access (para configurar Cognito y API Gateway)

### 1. Configurar AWS

Seguir `docs/aws-setup.md` para crear:
- Cognito User Pool + App Client
- API Gateway REST API
- Lambda Pre Token Generation

### 2. Variables de entorno

```bash
cp .env.example .env
# Completar con valores de AWS
```

### 3. Docker Compose

```bash
docker compose up --build
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| MongoDB | mongodb://localhost:27017 |

### 4. Sin Docker

**Backend:**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app/main.py
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Variables de entorno

Copiar `.env.example` y completar:

```env
# Backend
APP_NAME=Classic Library API
APP_ENV=development
MONGO_URI=mongodb://mongodb:27017
MONGO_DATABASE=classic_library
FRONTEND_URL=http://localhost:5173
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_XXXXXXXXX
COGNITO_APP_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
VITE_COGNITO_DOMAIN=classic-library.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=xxxxxxxxxxxxxxxxxxxxxxxxxx
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_REGION=us-east-1
```

Nunca commitear `.env`. Está en `.gitignore`.

## API REST

Todas las rutas usan el prefijo `/api/v1`.

### Públicas (sin autenticación)

```text
GET    /api/v1/books              # Listar libros
GET    /api/v1/books/{id}         # Obtener libro
GET    /api/v1/authors            # Listar autores
GET    /api/v1/authors/{id}       # Obtener autor
GET    /api/v1/authors/{id}/books # Libros de un autor
GET    /api/v1/health             # Health check
```

### Protegidas (requieren JWT admin)

```text
POST   /api/v1/books              # Crear libro
PUT    /api/v1/books/{id}         # Actualizar libro
DELETE /api/v1/books/{id}         # Eliminar libro
POST   /api/v1/authors            # Crear autor
PUT    /api/v1/authors/{id}       # Actualizar autor
DELETE /api/v1/authors/{id}       # Eliminar autor
```

### Autenticación

```text
GET    /api/v1/auth/me            # Usuario autenticado (requiere token)
```

## Licencia

Proyecto desarrollado con fines académicos y de demostración.
