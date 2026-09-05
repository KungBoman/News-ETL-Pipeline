from contextlib import asynccontextmanager

import psycopg
from fastapi import FastAPI

from src.load import create_connection
from src.logger import get_logger
from src.routers import articles, health, pipeline_runs

logger = get_logger(__name__)


def ensure_database_connection() -> bool:
    try:
        connection = create_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        connection.close()

        logger.info("Database connection verified")
        return True

    except psycopg.Error:
        logger.exception("Could not verify database connection")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not ensure_database_connection():
        raise RuntimeError("Database connection failed")

    yield


app = FastAPI(
    title="Swedish News ETL API",
    lifespan=lifespan,
)

app.include_router(articles.router)
app.include_router(health.router)
app.include_router(pipeline_runs.router)


@app.get("/")
def root():
    return {
        "name": "Swedish News ETL API",
        "docs": "/docs",
        "endpoints": {
            "articles": "/articles",
            "health": "/health",
            "pipeline-runs": "/pipeline-runs",
        },
    }
