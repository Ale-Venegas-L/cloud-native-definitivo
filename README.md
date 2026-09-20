# Classic Library

Biblioteca web de literatura clasica. MVP full-stack desarrollado como proyecto academico.

## Stack

| Capa | Tecnologia |
|---|---|
| Frontend | Vue 3.5, TypeScript 6, Vite 8, Tailwind CSS 4 |
| Backend | Python 3.14, FastAPI, Pydantic, PyMongo |
| Base de datos | MongoDB 7 |
| Autenticacion | AWS Cognito (OAuth 2.0 PKCE) |
| API Gateway | AWS API Gateway REST (Terraform) |
| Infraestructura | AWS EC2 (Terraform) |
| CI/CD | GitHub Actions |
| Contenedores | Docker, Docker Compose |

## Arquitectura

```text
Frontend (Vue 3)
   |
   | OAuth 2.0 / PKCE
   v
AWS Cognito (User Pool)
   |
   | JWT
   v
EC2 Instance
   |-- Frontend (nginx:80)
   |-- Backend (FastAPI:8000) --> MongoDB
   +-- API Gateway REST --> Backend
```

Modulos del backend: `auth`, `books`, `authors`. Cada modulo sigue el patron router -> service -> repository.

## Estado actual

### Implementado

| Componente | Estado |
|---|---|
| Frontend Vue 3 | Completo - catalogo publico, admin CRUD, auth Cognito PKCE |
| Backend FastAPI | Completo - modulos auth/books/authors, CORS, health |
| MongoDB | Completo - conexion, seed data, mongomock fallback |
| Cognito JWT verification | Completo - JWKS, issuer/audience validation, custom claims |
| Docker Compose | Completo - 3 servicios (mongodb, backend, frontend) |
| Tests backend | Completos - pytest + coverage |
| Tests frontend | Completos - Vitest + Vue Test Utils |
| AWS API Gateway | Implementado - Terraform REST API + CORS + Authorizer |
| Despliegue cloud | Implementado - EC2 via Terraform + GitHub Actions |
| CI/CD | Implementado - `.github/workflows/deploy.yml` (push a `aws`) |
| SHA-256 polyfill | Implementado - crypto.subtle fallback para HTTP |

### Pendiente

| Componente | Estado |
|---|---|
| Google Identity Provider | Requiere setup manual en Google Cloud Console |
| Lambda Pre Token Generation | Requiere permisos IAM (habilitar con `enable_cognito=true`) |
| WAF | No implementado |

## Requisitos - Prueba 1

### Criterios de evaluacion

1. Creacion de instancia de API Manager en funcionamiento en la plataforma cloud.
2. Configuracion del API Manager para llamar a los endpoints del backend.
3. Frontend consume endpoints a traves del API Manager correctamente configurado.
4. API Manager valida JWT: rechaza peticiones invalidas, acepta las correctas.
5. Creacion del tenant en IDaaS con usuarios registrados.
6. Frontend utiliza OAuth 2.0/OpenID Connect para iniciar sesion y obtener JWT valido.
7. Backend y frontend desplegados, activos e integrados en la nube.

### Indicadores de evaluacion

| Indicador | Descripcion |
|---|---|
| Rutas API Manager | Todas las rutas creadas y dirigidas a los microservicios correspondientes |
| CORS API Manager | Configurado de forma segura, origenes permitidos definidos correctamente |
| Tenant IDaaS | Tenant creado con usuarios de prueba, roles, politicas y parametros |
| Aplicacion IDaaS | Registrada con clientId, URIs de redireccion, roles y scopes |
| Flujo usuario | Registro e inicio de sesion funcional, tokens con claims esperados |
| OIDC PKCE | Authorization Code con PKCE: code verifier, code challenge, state, nonce |
| Validacion JWT API Manager | Todas las rutas aplican validacion JWT, verifica issuer y audience |
| Evidencia de rutas | Llamadas con y sin token, respuestas 200/401/403 coherentes |

## Decisiones de arquitectura

- `docs/architecture/ADR-001-firebase-authentication.md` - Decision original (Firebase)
- `docs/architecture/ADR-002-cognito-migration.md` - Migracion a Cognito

## Estructura del proyecto

```text
cloud-native-definitivo/
├── backend/                    # FastAPI REST API
│   ├── app/
│   │   ├── main.py             # Entry point, CORS, lifespan
│   │   ├── core/               # Config, database
│   │   ├── modules/            # auth, books, authors
│   │   └── shared/             # Seed data
│   ├── scripts/                # set_admin.py
│   ├── tests/                  # pytest
│   ├── Dockerfile.prod
│   └── requirements.txt
│
├── frontend/                   # Vue 3 SPA
│   ├── src/
│   │   ├── composables/        # useAuth, useTheme, useScrollReveal
│   │   ├── components/         # Pages, UI, views, modals
│   │   ├── services/           # api.ts (HTTP client)
│   │   ├── router/             # Rutas + guards
│   │   ├── lib/                # cognito.ts (SHA-256 polyfill incluido)
│   │   └── types/              # domain.ts
│   ├── Dockerfile.prod
│   └── package.json
│
├── infra/                      # Terraform
│   ├── main.tf                 # EC2 + Security Group + Key Pair
│   ├── cognito.tf              # User Pool, App Client (opcional)
│   ├── lambda.tf               # Lambda Pre Token Generation (opcional)
│   ├── api_gateway.tf          # REST API + CORS + Authorizer
│   ├── variables.tf            # Variables de entrada
│   ├── outputs.tf              # Outputs de Terraform
│   ├── user_data.sh            # Setup de la instancia
│   └── lambda/                 # Codigo Lambda
│
├── docs/
│   ├── aws-setup.md            # Guia configuracion AWS
│   └── architecture/
│
├── .github/workflows/deploy.yml  # CI/CD
├── docker-compose.prod.yml
└── DEPLOY.md                   # Documentacion de deploy
```

## Arranque rapido

### Requisitos

- Git, Python 3.14+, Node.js 22+, Docker Desktop
- AWS Academy account (para Cognito + EC2)

### 1. Configurar secrets de GitHub

Ver `DEPLOY.md` para la guia completa. Resumen rapido:

```bash
# SSH
gh secret set SSH_PRIVATE_KEY < ~/.ssh/classic-library-key

# AWS (cada laboratorio)
gh secret set AWS_ACCESS_KEY_ID
gh secret set AWS_SECRET_ACCESS_KEY
gh secret set AWS_SESSION_TOKEN

# Cognito (valores fijos)
gh secret set COGNITO_USER_POOL_ID <<< "us-east-1_GPg9HQGJP"
gh secret set COGNITO_APP_CLIENT_ID <<< "6e10hnmqf023ioa06qo72nejbd"
gh secret set COGNITO_DOMAIN <<< "us-east-1gpg9hqgjp"
```

### 2. Deploy

```bash
git push origin aws
```

### 3. Variables de entorno (desarrollo local)

```bash
cp .env.example .env
# Completar con valores de Cognito
```

## Variables de entorno

### Backend (.env)

```env
MONGO_URI=mongodb://mongodb:27017
MONGO_DATABASE=classic_library
FRONTEND_URL=http://localhost:5173
COGNITO_REGION=us-east-1
COGNITO_USER_POOL_ID=us-east-1_GPg9HQGJP
COGNITO_APP_CLIENT_ID=6e10hnmqf023ioa06qo72nejbd
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_COGNITO_DOMAIN=us-east-1gpg9hqgjp.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=6e10hnmqf023ioa06qo72nejbd
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_REGION=us-east-1
```

Nunca commitear `.env`. Esta en `.gitignore`.

## API REST

Todas las rutas usan el prefijo `/api/v1`.

### Publicas (sin autenticacion)

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

### Autenticacion

```text
GET    /api/v1/auth/me            # Usuario autenticado (requiere token)
```

## Licencia

Proyecto desarrollado con fines academicos y de demostracion.
