from src.extract import extract_rss, SVT_RSS_URL
from src.transform import transform_articles
from src.validate import validate_articles
from src.load import create_connection, load_articles
from src.config import RSS_SOURCES


def main() -> None:
    articles = []
    for source in RSS_SOURCES:
        source_articles = extract_rss(
            source["url"],
            source["name"],
        )

        articles.extend(source_articles)

    print(f"Extracted: {len(articles)} articles")

    transformed_articles = transform_articles(articles)
    print(f"Transformed: {len(transformed_articles)} articles")

    valid_articles = validate_articles(transformed_articles)
    print(f"Valid: {len(valid_articles)} articles")

    politics_articles = [
        a for a in valid_articles
        if a["is_politics_related"]
    ]

    connection = create_connection()

    try:
        loaded_articles = load_articles(connection, valid_articles, commit=True)
        print(f"Loaded: {loaded_articles} articles")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
