

from src.models import Article


def clean_article(article: Article) -> Article:
    cleaned_article = article.copy()

    cleaned_article["title"] = cleaned_article["title"].strip()
    cleaned_article["url"] = cleaned_article["url"].strip()

    description = cleaned_article.get("description")
    if isinstance(description, str):
        description = description.strip()
    cleaned_article["description"] = description or None

    author = cleaned_article.get("author")
    if isinstance(author, str):
        author = author.strip()
    cleaned_article["author"] = author or None

    category = cleaned_article.get("category")
    if isinstance(category, str):
        category = category.strip()
    cleaned_article["category"] = category or None

    return cleaned_article


def standardize_article(article: Article) -> Article:
    return article


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


def deduplicate_articles(articles: list[Article]) -> list[Article]:
    seen_urls = set()
    unique_articles = []

    for article in articles:
        url = article["url"]

        if url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)

    return unique_articles


def transform_articles(articles: list[Article]) -> list[Article]:
    transformed_articles = []

    for article in articles:
        article = clean_article(article)
        article = standardize_article(article)
        article = enrich_article(article)

        transformed_articles.append(article)

    return deduplicate_articles(transformed_articles)
