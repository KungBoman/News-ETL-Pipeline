"""
Endpoints for browsing and fetching articles.
"""

from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel

from src.load import try_create_connection
from src.repository.articles import get_articles


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
def get_articles_endpoint() -> list[ArticleResponse]:
    connection = try_create_connection()

    try:
        rows = get_articles(connection)

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
