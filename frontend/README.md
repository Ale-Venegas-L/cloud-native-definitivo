# Classic Library — Frontend

Aplicación Vue 3 que consume la API REST de Classic Library. Permite navegar el catálogo público de literatura clásica y, para administradores autenticados, gestionar libros y autores mediante CRUD.

## Stack

| Herramienta | Versión |
|---|---|
| Vue | 3.5 |
| TypeScript | 6.0 |
| Vite | 8.2 |
| Tailwind CSS | 4.3 |
| Vue Router | 5.2 |
| GSAP | 3.15 |
| Vitest | 3.0 |

## Estructura

```text
src/
├── main.ts                          # Punto de entrada
├── App.vue                          # Raíz del componente
├── style.css                        # Estilos globales (Tailwind)
│
├── lib/
│   └── cognito.ts                   # Configuración Cognito, PKCE, token exchange
│
├── composables/
│   ├── useAuth.ts                   # Estado de autenticación, login/logout
│   ├── useTheme.ts                  # Control de tema claro/oscuro
│   └── useScrollReveal.ts           # Animaciones de scroll con GSAP
│
├── services/
│   └── api.ts                       # Cliente HTTP con inyección de token
│
├── types/
│   └── domain.ts                    # Interfaces Author, Book, payloads
│
├── data/
│   └── editions.ts                  # Datos estáticos de ediciones
│
├── router/
│   ├── index.ts                     # Definición de rutas y guards
│   └── __tests__/
│       └── router.test.ts
│
├── assets/                          # Imágenes y recursos estáticos
│
└── components/
    ├── views/
    │   ├── public.vue               # Layout de rutas públicas
    │   └── admin.vue                # Layout de rutas administrativas
    │
    ├── pages/
    │   ├── public/
    │   │   ├── home.vue             # Hero y portada principal
    │   │   ├── books.vue            # Catálogo con filtros y búsqueda
    │   │   └── editions.vue         # Ediciones especiales
    │   ├── auth/
    │   │   ├── login.vue            # Inicio de sesión (redirige a Cognito)
    │   │   ├── callback.vue         # Callback post-autenticación
    │   │   └── unauthorized.vue     # Acceso denegado
    │   ├── admin/
    │   │   ├── panel.vue            # Dashboard administrativo
    │   │   └── stock.vue            # CRUD de libros y autores
    │   └── __tests__/
    │       ├── books.test.ts
    │       └── home.test.ts
    │
    ├── composables/
    │   ├── modal-author.vue         # Modal de información del autor
    │   └── modal-book.vue           # Modal de información del libro
    │
    └── UI/
        ├── BaseBadge.vue
        ├── BaseButton.vue
        ├── BaseCard.vue
        ├── BaseInput.vue
        ├── BaseModal.vue
        ├── BookArtwork.vue
        ├── BookCover.vue
        ├── ContentState.vue
        ├── EditorialCover.vue
        ├── ScrollBookmark.vue
        ├── ThemeToggle.vue
        ├── navbar.vue
        ├── sidebar.vue
        ├── footer.vue
        └── __tests__/
            ├── BaseBadge.test.ts
            ├── BaseButton.test.ts
            ├── BaseCard.test.ts
            ├── BaseInput.test.ts
            └── BaseModal.test.ts
```

## Autenticación

El frontend utiliza **AWS Cognito** con flujo **OAuth 2.0 Authorization Code + PKCE**.

### Flujo

```text
1. Usuario clickea "Iniciar sesión"
2. Frontend genera code_verifier y code_challenge (S256)
3. Redirect a Cognito Hosted UI → Google Sign-In
4. Cognito redirige de vuelta con ?code=xxx&state=yyy
5. Frontend intercambia code por tokens (POST /oauth2/token)
6. Access token se almacena en sessionStorage
7. Custom claims (admin, permissions) se leen del JWT
8. Si es admin → /admin, si no → /unauthorized
```

### Capa de API (`services/api.ts`)

- Todas las llamadas al backend pasan por `apiRequest<T>(path, options)`.
- Cuando `options.authenticated` es `true`, se obtiene el access token de sessionStorage y se envía como `Authorization: Bearer <token>`.

### Route guards (`router/index.ts`)

- Las rutas con `meta.requiresAdmin` verifican que el usuario esté autenticado y tenga `custom:admin === true`.
- Si no está autenticado → redirige a `/login`.
- Si no es admin → redirige a `/unauthorized`.

## Rutas

| Ruta | Componente | Acceso |
|---|---|---|
| `/` | `home.vue` | Público |
| `/books` | `books.vue` | Público |
| `/editions` | `editions.vue` | Público |
| `/login` | `login.vue` | Público |
| `/callback` | `callback.vue` | Público |
| `/unauthorized` | `unauthorized.vue` | Público |
| `/admin` | `panel.vue` | Admin |
| `/admin/stock` | `stock.vue` | Admin |

## Variables de entorno

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_COGNITO_DOMAIN=classic-library.auth.us-east-1.amazoncognito.com
VITE_COGNITO_CLIENT_ID=your-app-client-id
VITE_COGNITO_REDIRECT_URI=http://localhost:5173/callback
VITE_COGNITO_REGION=us-east-1
```

Copiar `.env.example` y completar los valores reales de AWS Cognito. Nunca commitear `.env`.

## Instalación

```bash
cd frontend
npm install
npm run dev
```

El frontend se ejecuta en `http://localhost:5173`.

## Scripts

| Comando | Descripción |
|---|---|
| `npm run dev` | Servidor de desarrollo Vite |
| `npm run build` | Build de producción (vue-tsc + vite build) |
| `npm run preview` | Vista previa del build |
| `npm run test` | Ejecutar tests (Vitest) |
| `npm run test:watch` | Tests en modo watch |
| `npm run test:coverage` | Tests con cobertura |
| `npm run lint` | Linting con ESLint |
| `npm run lint:fix` | Linting con auto-fix |
| `npm run format` | Formatear con Prettier |

## Tests

Tests unitarios y de componente con **Vitest** + **Vue Test Utils**:

- `components/__tests__/` — Tests de componentes UI (BaseBadge, BaseButton, BaseCard, BaseInput, BaseModal)
- `pages/__tests__/` — Tests de páginas (books, home)
- `router/__tests__/` — Tests de enrutamiento

```bash
npm run test
```

## Docker

```bash
docker compose up --build frontend
```

El servicio frontend expone el puerto 5173 y depende del servicio backend.
