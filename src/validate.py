
def validate_article(article: dict) -> bool:
    required_fields = [
        "source",
        "title",
        "url",
        "published_at",
    ]

    for field in required_fields:
        if not article.get(field):
            return False

    return True


def validate_articles(articles: list[dict]) -> list[dict]:
    valid_articles = []

    for article in articles:
        if validate_article(article):
            valid_articles.append(article)

    return valid_articles
