import psycopg

from src.logger import get_logger
from src.models import Article
import src.common_util as cu

logger = get_logger(__name__)


def create_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=cu.get_required_env("DB_HOST"),
        port=cu.get_required_env("DB_PORT"),
        dbname=cu.get_required_env("DB_NAME"),
        user=cu.get_required_env("DB_USER"),
        password=cu.get_required_env("DB_PASSWORD"),
    )


def load_article(connection: psycopg.Connection, article: Article, commit: bool) -> bool:
    query = """
        INSERT INTO articles (
            source,
            title,
            description,
            url,
            published_at,
            author,
            category,
            is_politics_related
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (url) DO NOTHING
        RETURNING id
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (
                article["source"],
                article["title"],
                article["description"],
                article["url"],
                article["published_at"],
                article["author"],
                article["category"],
                article["is_politics_related"],
            ),
        )

        result = cursor.fetchone()

    if commit:
        connection.commit()

    return result is not None


def load_articles(connection: psycopg.Connection, articles: list[Article], commit: bool) -> None:
    inserted = 0
    duplicates = 0

    try:
        for article in articles:
            was_inserted = load_article(connection, article, commit=False)

            if was_inserted:
                inserted += 1
            else:
                duplicates += 1

        if commit:
            connection.commit()

        logger.info(
            f"Loaded {inserted} articles, "
            f"skipped {duplicates} duplicates"
        )

        return inserted

    except Exception:
        connection.rollback()
        logger.exception("Failed to load articles")
        raise
