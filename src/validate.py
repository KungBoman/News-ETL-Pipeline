from src.logger import get_logger
from src.models import Article

logger = get_logger(__name__)


def validate_article(article: Article) -> bool:
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


def validate_articles(articles: list[Article]) -> list[Article]:
    valid_articles = []

    for article in articles:
        if validate_article(article):
            valid_articles.append(article)

    logger.info(
        f"Validated {len(valid_articles)}/{len(articles)} articles")

    return valid_articles
