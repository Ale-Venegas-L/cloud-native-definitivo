# Classic Library — Frontend

Aplicación Vue 3 que consume la API REST de Classic Library. Permite navegar el catálogo público de literatura clásica y, para administradores autenticados, gestionar libros y autores mediante CRUD.

## Stack

| Herramienta | Versión |
|---|---|
| Vue | 3.5 |
| TypeScript | 6.0 |
| Vite | 8.2 |
| Tailwind CSS | 4.3 |
| Firebase SDK | 12.18 |
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
│   └── firebase.ts                  # Inicialización de Firebase Auth
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
    │   │   ├── login.vue            # Inicio de sesión con Google
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

El frontend utiliza **Firebase Authentication** con **Google Sign-In** como proveedor de identidad.

### Flujo

```text
Usuario clickea "Continuar con Google"
  → Firebase muestra popup de Google OAuth
  → Firebase almacena sesión localmente
  → onAuthStateChanged notifica el cambio de estado
  → getIdTokenResult() lee custom claims (admin)
  → Si es admin → redirige a /admin
  → Si no es admin → redirige a /unauthorized
```

### Capa de API (`services/api.ts`)

- Todas las llamadas al backend pasan por `apiRequest<T>(path, options)`.
- Cuando `options.authenticated` es `true`, se obtiene el token Firebase y se envía como `Authorization: Bearer <token>`.
- Si la API responde 401, se fuerza refresh del token y se reintenta la petición automáticamente.

### Route guards (`router/index.ts`)

- Las rutas con `meta.requiresAdmin` verifican que el usuario esté autenticado y tenga el claim `admin: true`.
- Si no está autenticado → redirige a `/login`.
- Si no es admin → redirige a `/unauthorized`.

## Rutas

| Ruta | Componente | Acceso |
|---|---|---|
| `/` | `home.vue` | Público |
| `/books` | `books.vue` | Público |
| `/editions` | `editions.vue` | Público |
| `/login` | `login.vue` | Público |
| `/unauthorized` | `unauthorized.vue` | Público |
| `/admin` | `panel.vue` | Admin |
| `/admin/stock` | `stock.vue` | Admin |

## Variables de entorno

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_FIREBASE_API_KEY=your-web-api-key
VITE_FIREBASE_AUTH_DOMAIN=colud-native.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=colud-native
VITE_FIREBASE_STORAGE_BUCKET=colud-native.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=17691843333
VITE_FIREBASE_APP_ID=1:17691843333:web:71a9e325b0288dda7e756c
VITE_FIREBASE_MEASUREMENT_ID=G-FHGRCXMNXV
```

Copiar `.env.example` y completar los valores reales. Nunca commitear `.env`.

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
