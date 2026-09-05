"""
Endpoints for browsing and fetching articles.
"""

from datetime import datetime

import psycopg
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from src.load import try_create_connection
from src.repository.articles import (
    get_article_by_id,
    get_article_stats,
    get_articles,
)


class ArticleResponse(BaseModel):
    id: int
    source: str
    title: str
    published_at: datetime
    text_url: str
    image_url: str | None
    summary: str | None
    author_name: str | None
    author_email: str | None
    category: str | None


class ArticleStatsResponse(BaseModel):
    total_articles: int
    politics_related: int
    articles_by_source: dict[str, int]


router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("/")
def get_articles_endpoint(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    source: str | None = None,
) -> list[ArticleResponse]:
    connection = try_create_connection()

    try:
        rows = get_articles(
            connection,
            limit=limit,
            offset=offset,
            source=source,
        )

        return [
            ArticleResponse(
                id=row[0],
                source=row[1],
                title=row[2],
                published_at=row[3],
                text_url=row[4],
                image_url=row[5],
                summary=row[6],
                author_name=row[7],
                author_email=row[8],
                category=row[9],
            )
            for row in rows
        ]

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

    finally:
        connection.close()


@router.get("/stats")
def get_article_stats_endpoint() -> ArticleStatsResponse:
    connection = try_create_connection()

    try:
        stats = get_article_stats(connection)
        return ArticleStatsResponse(**stats)

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

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
            published_at=row[3],
            text_url=row[4],
            image_url=row[5],
            summary=row[6],
            author_name=row[7],
            author_email=row[8],
            category=row[9],
        )

    except psycopg.Error:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

    finally:
        connection.close()
