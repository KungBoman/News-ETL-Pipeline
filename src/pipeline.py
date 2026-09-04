from src.config import RSS_SOURCES
from src.extract import extract_rss
from src.load import load_articles, try_create_connection
from src.transform import transform_articles
from src.validate import validate_articles


def run_pipeline() -> dict[str, int]:
    articles = []

    for source in RSS_SOURCES:
        source_articles = extract_rss(
            source["url"],
            source["name"]
        )

        articles.extend(source_articles)

    extracted_count = len(articles)

    transformed_articles = transform_articles(articles)
    transformed_count = len(transformed_articles)

    valid_articles = validate_articles(transformed_articles)
    valid_count = len(valid_articles)

    connection = try_create_connection()

    try:
        loaded_count = load_articles(connection, valid_articles, commit=True)
    finally:
        connection.close()

    return {
        "extracted": extracted_count,
        "transformed": transformed_count,
        "valid": valid_count,
        "loaded": loaded_count,
    }
