from src.models import Article


def clean_article(article: Article) -> Article:
    # TODO: check up if we actually prefer to reference the copy or the parameter throughout the function
    cleaned_article = article.copy()

    cleaned_article["title"] = cleaned_article["title"].strip()
    cleaned_article["text_url"] = cleaned_article["text_url"].strip()

    summary = cleaned_article.get("summary")
    if isinstance(summary, str):
        summary = summary.strip()
    cleaned_article["summary"] = summary or None

    author_name = cleaned_article.get("author_name")
    if isinstance(author_name, str):
        author_name = author_name.strip()
    cleaned_article["author_name"] = author_name or None

    author_email = cleaned_article.get("author_email")
    if isinstance(author_email, str):
        author_email = author_email.strip()
    cleaned_article["author_email"] = author_email or None

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
                enriched_article["summary"],
                enriched_article["text_url"],
            ],
        )
    ).lower()

    category_keywords = {
        "politics": [
            "val",
            "regering",
            "riksdag",
            "parti",
            "minister",
            "statsminister",
            "politiker",
            "politik",
        ],
        "sport": [
            "fotboll",
            "hockey",
            "ishockey",
            "sport",
            "match",
            "landslag",
            "allsvenskan",
        ],
        "economy": [
            "ekonomi",
            "börsen",
            "ränta",
            "inflation",
            "företag",
            "aktie",
        ],
        "technology": [
            "teknik",
            "ai",
            "artificiell intelligens",
            "apple",
            "google",
            "microsoft",
        ],
    }

    category = "other"

    for name, keywords in category_keywords.items():
        if any(keyword in text for keyword in keywords):
            category = name
            break

    enriched_article["category"] = category

    return enriched_article


def deduplicate_articles(articles: list[Article]) -> list[Article]:
    seen_urls = set()
    unique_articles = []

    for article in articles:
        text_url = article["text_url"]

        if text_url not in seen_urls:
            seen_urls.add(text_url)
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
