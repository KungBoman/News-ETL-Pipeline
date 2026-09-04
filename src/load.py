import time

import psycopg

import src.common_util as cu
from src.logger import get_logger
from src.models import Article

logger = get_logger(__name__)


def create_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=cu.get_required_env("DB_HOST"),
        port=cu.get_required_env("DB_PORT"),
        dbname=cu.get_required_env("DB_NAME"),
        user=cu.get_required_env("DB_USER"),
        password=cu.get_required_env("DB_PASSWORD"),
        connect_timeout=1,
    )


def try_create_connection(
    max_attempts: int = 5,
    retry_delay: int = 5,
) -> psycopg.Connection:

    for attempt in range(1, max_attempts + 1):
        logger.info(
            f"Connecting to PostgreSQL... "
            f"{
                f"(attempt {attempt}/{max_attempts})"
                if attempt > 1 else ""
            }"
        )

        try:
            connection = create_connection()

            logger.info("Connected to PostgreSQL")
            return connection

        except psycopg.OperationalError as error:
            if attempt == max_attempts:
                logger.error(
                    f"Could not connect to PostgreSQL after "
                    f"{max_attempts} attempts: {error}"
                )
                raise

            logger.warning(
                f"Could not connect to PostgreSQL. "
                f"Retrying in {retry_delay} seconds..."
            )

            time.sleep(retry_delay)


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
