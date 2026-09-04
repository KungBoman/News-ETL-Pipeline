"""
Endpoints for browsing and fetching articles.
"""

from datetime import datetime
import psycopg
from fastapi import APIRouter
from pydantic import BaseModel

from src.load import try_create_connection


class ArticleResponse(BaseModel):
    id: int
    source: str
    title: str
    description: str | None
    url: str
    published_at: datetime
    author: str | None
    category: str | None
    is_politics_related: bool


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/get")
def get_articles() -> list[ArticleResponse]:
    connection = try_create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    id,
                    source,
                    title,
                    description,
                    url,
                    published_at,
                    author,
                    category,
                    is_politics_related
                FROM articles
                ORDER BY published_at DESC
            """)

            rows = cursor.fetchall()

        return [
            ArticleResponse(
                id=row[0],
                source=row[1],
                title=row[2],
                description=row[3],
                url=row[4],
                published_at=row[5],
                author=row[6],
                category=row[7],
                is_politics_related=row[8],
            )
            for row in rows
        ]

    finally:
        connection.close()
