from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import get_database, close_database, is_mock
from app.modules.books.router import router as books_router
from app.modules.authors.router import router as authors_router
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


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books_router)
app.include_router(authors_router)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "mock_db": is_mock()
    }
