from src.extract import extract_rss, SVT_RSS_URL
from src.transform import transform_articles
from src.validate import validate_articles
from src.load import create_connection, load_articles


def main() -> None:
    articles = extract_rss(SVT_RSS_URL, "SVT")
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
        load_articles(connection, valid_articles, commit=True)
        print(f"Loaded: {len(valid_articles)} articles")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
