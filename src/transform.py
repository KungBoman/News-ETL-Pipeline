from datetime import datetime

from src.models import Article


def clean_article(article: Article) -> Article:
    cleaned_article = article.copy()

    for field in ["title", "description", "url", "author", "category"]:
        value = cleaned_article.get(field)

        if isinstance(value, str):
            value = value.strip()

        cleaned_article[field] = value if value else None

    return cleaned_article


def standardize_article(article: Article) -> Article:
    standardized_article = article.copy()

    published_at = standardized_article["published_at"]

    if isinstance(published_at, str):
        standardized_article["published_at"] = datetime.strptime(
            published_at,
            "%a, %d %b %Y %H:%M:%S %z"
        )

    return standardized_article


def enrich_article(article: Article) -> Article:
    enriched_article = article.copy()

    text = " ".join(
        filter(
            None,
            [
                enriched_article["title"],
                enriched_article["description"],
            ],
        )
    ).lower()

    politics_keywords = [
        "val",
        "regering",
        "riksdag",
        "parti",
        "minister",
        "statsminister",
        "politiker",
        "politik",
    ]

    enriched_article["is_politics_related"] = any(
        keyword in text
        for keyword in politics_keywords
    )

    return enriched_article


def transform_articles(articles: list[Article]) -> list[Article]:
    transformed_articles = []

    for article in articles:
        article = clean_article(article)
        article = standardize_article(article)
        article = enrich_article(article)

        transformed_articles.append(article)

    return transformed_articles
