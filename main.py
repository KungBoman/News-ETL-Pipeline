from src.extract import extract_rss, SVT_RSS_URL
from src.transform import transform_articles
from src.validate import validate_articles


def main() -> None:
    articles = extract_rss(SVT_RSS_URL, "SVT")
    transformed_articles = transform_articles(articles)
    valid_articles = validate_articles(transformed_articles)
    politics_articles = [
        a for a in valid_articles
        if a["is_politics_related"]
    ]

    print(f"Extracted: {len(articles)}")
    print(f"Valid: {len(valid_articles)}")
    print(f"Politics related: {len(politics_articles)}")

    for key, value in transformed_articles[0].items():
        print(f"\n{key}:")
        print(value)


if __name__ == "__main__":
    main()
