from datetime import datetime


def clean_article(article: dict) -> dict:
    clean_article = article.copy()

    for field in ["title", "description", "url", "author", "category"]:
        value = clean_article.get(field)

        if isinstance(value, str):
            value = value.strip()

        clean_article[field] = value if value else None

    return clean_article


def standardize_article(article: dict) -> dict:
    std_article = article.copy()

    published_at = std_article.get("published_at")

    if published_at:
        std_article["published_at"] = datetime.strptime(
            published_at,
            "%a, %d %b %Y %H:%M:%S %z"
        )

    return std_article


def enrich_article(article: dict) -> dict:
    enriched_article = article.copy()

    text = " ".join(
        filter(
            None,
            [
                enriched_article.get("title"),
                enriched_article.get("description"),
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


def transform_articles(articles: list[dict]) -> list[dict]:
    transformed_articles = []

    for article in articles:
        article = clean_article(article)
        article = standardize_article(article)
        article = enrich_article(article)

        transformed_articles.append(article)

    return transformed_articles
