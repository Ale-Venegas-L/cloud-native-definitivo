# Classic Library

Biblioteca web de literatura clásica. MVP full-stack desarrollado como proyecto académico.

## Stack

| Capa | Tecnología |
|---|---|
| Frontend | Vue 3.5, TypeScript 6, Vite 8, Tailwind CSS 4 |
| Backend | Python 3.14, FastAPI, Pydantic, PyMongo |
| Base de datos | MongoDB 7 |
| Autenticación | Firebase Authentication (Google Sign-In) |
| Contenedores | Docker, Docker Compose |
| Infraestructura | Terraform (AWS) — en progreso |

## Arquitectura

```text
Frontend (Vue 3)
   │
   │ HTTP / JSON + Bearer Token
   v
FastAPI REST API (/api/v1)
   │
   v
MongoDB
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

## Estado actual

### Implementado

| Componente | Estado |
|---|---|
| Frontend Vue 3 | Completo — catálogo público, admin CRUD, auth |
| Backend FastAPI | Completo — módulos auth/books/authors, CORS, health |
| MongoDB | Completo — conexión, seed data, mongomock fallback |
| Firebase Auth | Completo — Google Sign-In, custom claims, verificación server-side |
| Docker Compose | Completo — 3 servicios (mongodb, backend, frontend) |
| Tests backend | Completos — pytest + coverage |
| Tests frontend | Completos — Vitest + Vue Test Utils |

### Pendiente (Prueba 1)

| Componente | Estado |
|---|---|
| AWS API Gateway | No implementado — sin archivos Terraform |
| IDaaS tenant (PKCE) | No implementado — se usa Firebase Auth con Google Sign-In |
| Despliegue cloud | No implementado — solo ejecución local vía docker-compose |
| CI/CD | No configurado — `.github/workflows/` vacío |
| Terraform IaC | No implementado — `infra/` vacío |
| WAF | No implementado |

### Roadmap

Ver `docs/ROADMAP.md` para el detalle de hitos.

| Hito | Descripción | Estado |
|---|---|---|
| Hito 1 | Fundación segura e identidad | En progreso |
| Hito 1.5 | Experiencia de interfaz | Completo |
| Hito 2 | Integridad del dominio | Planificado |
| Hito 3 | Calidad y delivery | Planificado |
| Hito 4 | AWS API Gateway | Planificado |

## Decisiones de arquitectura

Ver `docs/architecture/ADR-001-firebase-authentication.md` para la decisión sobre Firebase Authentication como proveedor de identidad.

## Estructura del proyecto

```text
MVP-AWS-DESARROLLO-CLOUD-NATIVE-I_004D-/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py             # Entry point, CORS, lifespan
│   │   ├── core/               # Config, database
│   │   ├── modules/            # auth, books, authors
│   │   └── shared/             # Seed data
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
│   │   ├── lib/                # firebase.ts
│   │   └── types/              # domain.ts
│   ├── Dockerfile
│   └── package.json
│
├── infra/                      # Terraform (AWS)
├── docs/
│   ├── ROADMAP.md
│   └── architecture/
├── design/                     # Assets de diseño
├── docker-compose.yml
├── firebase.json
└── .env.example
```

## Arranque rápido

### Requisitos

- Git, Python 3.14+, Node.js 22+, Docker Desktop

### Con Docker Compose (recomendado)

```bash
cp .env.example .env    # Completar variables de entorno
docker compose up --build
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| MongoDB | mongodb://localhost:27017 |

### Sin Docker

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
FIREBASE_PROJECT_ID=colud-native
FIREBASE_CHECK_REVOKED=false

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
VITE_FIREBASE_API_KEY=your-web-api-key
VITE_FIREBASE_AUTH_DOMAIN=colud-native.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=colud-native
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
