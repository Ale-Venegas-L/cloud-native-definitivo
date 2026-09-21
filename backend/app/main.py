from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import close_database, get_database, get_client, is_mock
from app.modules.auth.router import router as auth_router
from app.modules.authors.router import router as authors_router
from app.modules.books.router import router as books_router
from app.shared.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_database()
    if is_mock():
        print("!MongoDB no disponible! — usando datos en memoria")
    else:
        print("✓  MongoDB conectado")
    seed_data()
    yield
    close_database()


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router, prefix=settings.API_V1_PREFIX)
app.include_router(authors_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)


@app.get(f"{settings.API_V1_PREFIX}/health", tags=["health"])
async def health():
    mongo_ok = False
    if not is_mock():
        try:
            client = get_client()
            if client:
                client.admin.command("ping")
                mongo_ok = True
        except Exception:
            pass
    return {"status": "ok", "mock_db": is_mock(), "mongo": mongo_ok}
