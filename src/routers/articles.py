"""
Endpoints for browsing and fetching articles.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.load import try_create_connection
from src.repository.articles import (
    get_article_by_id,
    get_articles,
)


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


@router.get("/")
def get_articles_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    source: str | None = None,
    is_politics_related: bool | None = None,
) -> list[ArticleResponse]:
    connection = try_create_connection()

    try:
        rows = get_articles(
            connection,
            limit=limit,
            offset=offset,
            source=source,
            is_politics_related=is_politics_related,
        )

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


@router.get("/{article_id}")
def get_article_by_id_endpoint(article_id: int) -> ArticleResponse:
    connection = try_create_connection()

    try:
        row = get_article_by_id(connection, article_id)

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Article not found",
            )

        return ArticleResponse(
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

    finally:
        connection.close()
