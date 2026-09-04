from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routers import (
    articles,
    health,
)


def ensure_database_connection() -> bool:
    return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_database_connection()
    yield


app = FastAPI(
    title="Swedish News ETL API",
    lifespan=lifespan,
)

app.include_router(articles.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {
        "name": "Swedish News ETL API",
        "docs": "/docs",
        "endpoints": {
            "articles": "/articles",
            "health": "/health",
        }
    }
