# Classic Library MVP

Biblioteca web de literatura clásica desarrollada como MVP Full Stack.

El sistema permite consultar obras clásicas organizadas por autor, país y año de publicación, además de proporcionar una interfaz administrativa para gestionar libros y autores mediante operaciones CRUD.

## Objetivo

Construir un MVP Full Stack que permita demostrar:

* Separación entre frontend, backend y persistencia.
* Comunicación mediante API REST.
* Intercambio de información en formato JSON.
* Operaciones CRUD.
* Persistencia de datos con MongoDB.
* Comunicación entre frontend y backend.
* Configuración de CORS.
* Preparación para una futura migración hacia AWS.

## Funcionalidades

### Vista pública

* Catálogo de libros.
* Visualización de portada.
* Búsqueda por título.
* Filtro por autor.
* Filtro por país.
* Filtro por año.
* Filtro por género.
* Información del libro.
* Modal reutilizable para visualizar información del autor.
* Biografía del autor.
* Listado de obras asociadas al autor.

### Vista administrativa

* Dashboard.
* Listado de libros.
* Crear libro.
* Editar libro.
* Eliminar libro.
* Listado de autores.
* Crear autor.
* Editar autor.
* Eliminar autor.

## Arquitectura

El sistema utiliza una arquitectura monolítica modular.

```text
Frontend
   |
   | HTTP / JSON
   v
FastAPI REST API
   |
   v
MongoDB
```

La aplicación se encuentra dividida en módulos internos independientes para mantener organizada la lógica del sistema.

```text
Backend
├── Books
└── Authors
```

## Stack tecnológico

### Frontend

* Vue 3
* TypeScript
* Tailwind CSS
* Vite
* GSAP
* Node.js como entorno de desarrollo

### Backend

* Python
* FastAPI
* Pydantic
* PyMongo

### Persistencia

* MongoDB

### Infraestructura

* Docker
* Docker Compose

### Herramientas

* Git
* GitHub
* Swagger
* Postman / Thunder Client
* Visual Studio Code

## Estructura del proyecto

```text
classic-library/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   │
│   │   ├── modules/
│   │   │   ├── books/
│   │   │   │   ├── router.py
│   │   │   │   ├── schemas.py
│   │   │   │   ├── service.py
│   │   │   │   └── repository.py
│   │   │   │
│   │   │   └── authors/
│   │   │       ├── router.py
│   │   │       ├── schemas.py
│   │   │       ├── service.py
│   │   │       └── repository.py
│   │   │
│   │   └── shared/
│   │
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.ts
│   │   ├── style.css
│   │   │
│   │   ├── composables/
│   │   │   └── useScrollReveal.ts
│   │   │
│   │   ├── router/
│   │   │   └── index.ts
│   │   │
│   │   ├── assets/
│   │   │
│   │   └── components/
│   │       ├── composables/
│   │       │   ├── modal-author.vue
│   │       │   └── modal-book.vue
│   │       │
│   │       ├── pages/
│   │       │   ├── public/
│   │       │   │   ├── home.vue
│   │       │   │   └── books.vue
│   │       │   │
│   │       │   └── admin/
│   │       │       ├── panel.vue
│   │       │       └── stock.vue
│   │       │
│   │       ├── UI/
│   │       │   ├── BaseBadge.vue
│   │       │   ├── BaseButton.vue
│   │       │   ├── BaseCard.vue
│   │       │   ├── BaseInput.vue
│   │       │   ├── BaseModal.vue
│   │       │   ├── navbar.vue
│   │       │   ├── sidebar.vue
│   │       │   └── footer.vue
│   │       │
│   │       └── views/
│   │           ├── public.vue
│   │           └── admin.vue
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   └── Dockerfile
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Modelo de datos

### Author

```json
{
  "_id": "ObjectId",
  "name": "Miguel de Cervantes",
  "country": "España",
  "birth_year": 1547,
  "death_year": 1616,
  "biography": "Novelista, poeta y dramaturgo español.",
  "image_url": "/authors/cervantes.webp"
}
```

### Book

```json
{
  "_id": "ObjectId",
  "title": "Don Quijote de la Mancha",
  "author_id": "ObjectId",
  "country": "España",
  "publication_year": 1605,
  "genre": "Novela",
  "description": "Obra clásica de la literatura española.",
  "cover_url": "/covers/don-quijote.webp"
}
```

## API REST

URL local:

```text
http://localhost:8000/api
```

### Books

```text
GET    /api/books
GET    /api/books/{id}
POST   /api/books
PUT    /api/books/{id}
DELETE /api/books/{id}
```

### Authors

```text
GET    /api/authors
GET    /api/authors/{id}
POST   /api/authors
PUT    /api/authors/{id}
DELETE /api/authors/{id}
```

### Libros de un autor

```text
GET /api/authors/{id}/books
```

## Instalación

### Requisitos

Tener instalado:

```text
Git
Python
Node.js
Docker Desktop
```

Comprobar instalaciones:

```bash
git --version
python --version
node --version
npm --version
docker --version
docker compose version
```

## Clonar repositorio

```bash
git clone URL_DEL_REPOSITORIO
cd classic-library
```

## Backend

Entrar al backend:

```bash
cd backend
```

Crear entorno virtual:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar:

```bash
fastapi dev app/main.py
```

Backend:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## Frontend

Entrar:

```bash
cd frontend
```

Instalar dependencias:

```bash
npm install
```

Ejecutar:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Variables de entorno

Backend:

```env
APP_NAME=Classic Library API
APP_ENV=development

MONGO_URI=mongodb://mongodb:27017
MONGO_DATABASE=classic_library

FRONTEND_URL=http://localhost:5173
```

Frontend:

```env
VITE_API_URL=http://localhost:8000/api
```

No se deben almacenar credenciales reales en Git.

Agregar `.env` a `.gitignore`.

## Docker

Levantar toda la aplicación:

```bash
docker compose up --build
```

Ejecutar en segundo plano:

```bash
docker compose up -d
```

Detener:

```bash
docker compose down
```

Detener y eliminar volumen de datos:

```bash
docker compose down -v
```

## Servicios locales

| Servicio | URL                        |
| -------- | -------------------------- |
| Frontend | http://localhost:5173      |
| Backend  | http://localhost:8000      |
| Swagger  | http://localhost:8000/docs |
| MongoDB  | mongodb://localhost:27017  |

## CORS

Durante el desarrollo se permite el frontend local:

```text
http://localhost:5173
```

El backend se ejecuta en:

```text
http://localhost:8000
```

La API deberá admitir:

```text
GET
POST
PUT
DELETE
OPTIONS
```

Headers principales:

```text
Content-Type
Authorization
```

## Pruebas

Antes de integrar completamente el frontend deben validarse los endpoints utilizando Swagger, Postman o Thunder Client.

Pruebas mínimas:

* GET de todos los libros.
* GET de un libro.
* POST de un libro.
* PUT de un libro.
* DELETE de un libro.
* GET de autores.
* GET de libros asociados a un autor.

## Flujo completo esperado

```text
Usuario
   ↓
Frontend (Vue 3)
   ↓
HTTP / JSON
   ↓
FastAPI
   ↓
Repository
   ↓
MongoDB
   ↓
FastAPI
   ↓
JSON
   ↓
Frontend (Vue 3)
```

## Roadmap

### Fase 0

Configuración inicial.

* Git.
* FastAPI.
* Vue 3 + Vite.
* Tailwind CSS.
* MongoDB.
* Docker.

### Fase 1

Persistencia.

* Conexión MongoDB.
* Colección Authors.
* Colección Books.
* Datos iniciales.

### Fase 2

CRUD Books.

* GET.
* GET ID.
* POST.
* PUT.
* DELETE.

### Fase 3

CRUD Authors.

* GET.
* GET ID.
* POST.
* PUT.
* DELETE.
* Obras del autor.

### Fase 4

Vista pública.

* Catálogo.
* Cards.
* Filtros.
* Buscador.

### Fase 5

Modal de autor.

* Biografía.
* Información personal.
* Obras asociadas.

### Fase 6

Vista administrativa.

* Dashboard.
* Gestión de libros.
* Gestión de autores.

### Fase 7

Integración.

* Frontend → API.
* API → MongoDB.
* CORS.
* Manejo de errores.

### Fase 8

Pruebas.

* Swagger.
* Postman.
* CRUD completo.
* Prueba extremo a extremo.

### Fase 9

Preparación AWS.

La arquitectura podrá evolucionar posteriormente hacia:

```text
Frontend publicado
       ↓
Amazon API Gateway
       ↓
AWS Lambda
       ↓
Amazon DynamoDB
```

El contrato REST deberá mantenerse en lo posible para minimizar cambios en el frontend.

## Estado del proyecto

```text
[x] Configuración
[x] MongoDB
[x] API Books
[x] API Authors
[x] Catálogo público
[x] Modal Authors
[x] Admin
[x] CRUD completo
[x] CORS
[x] Docker
[ ] Testing
[x] Documentación
```

## Licencia

Proyecto desarrollado con fines académicos y de demostración.
