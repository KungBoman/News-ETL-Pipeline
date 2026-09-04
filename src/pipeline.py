from datetime import datetime, timezone

from src.config import RSS_SOURCES
from src.extract import extract_rss
from src.load import load_articles, try_create_connection
from src.logger import get_logger
from src.models import Article
from src.repository.pipeline_runs import (
    create_pipeline_run,
    finish_pipeline_run,
)
from src.transform import transform_articles
from src.validate import validate_articles

logger = get_logger(__name__)


def run_pipeline() -> dict[str, int]:
    started_at = datetime.now(timezone.utc)

    connection = try_create_connection()

    run_id = create_pipeline_run(connection, started_at)

    extracted_count: int | None = None
    transformed_count: int | None = None
    valid_count: int | None = None
    loaded_count: int | None = None

    try:
        articles: list[Article] = []

        for source in RSS_SOURCES:
            try:
                source_articles = extract_rss(source["url"], source["name"])
                articles.extend(source_articles)
            except Exception:
                logger.exception(
                    f"Failed to extract articles from {source['name']}. "
                    "Continuing with remaining sources."
                )
                continue

        extracted_count = len(articles)

        transformed_articles = transform_articles(articles)
        transformed_count = len(transformed_articles)

        valid_articles = validate_articles(transformed_articles)
        valid_count = len(valid_articles)

        loaded_count = load_articles(
            connection,
            valid_articles,
            commit=True,
        )

        finish_pipeline_run(
            connection,
            run_id,
            datetime.now(timezone.utc),
            "success",
            extracted_count,
            transformed_count,
            valid_count,
            loaded_count,
        )

        return {
            "extracted": extracted_count,
            "transformed": transformed_count,
            "valid": valid_count,
            "loaded": loaded_count,
        }

    except Exception as error:
        finish_pipeline_run(
            connection,
            run_id,
            datetime.now(timezone.utc),
            "failed",
            extracted_count,
            transformed_count,
            valid_count,
            loaded_count,
            str(error),
        )
        raise

    finally:
        connection.close()
