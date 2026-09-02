import psycopg

from src.models import Article


def create_connection() -> psycopg.Connection:
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="news",
        user="news_user",
        password="news_password",
    )


def load_article(connection: psycopg.Connection, article: Article, commit: bool) -> None:
    query = """
        INSERT INTO articles (
            source,
            title,
            description,
            url,
            published_at,
            author,
            category,
            is_politics_related
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s
        )
        ON CONFLICT (url) DO NOTHING
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (
                article["source"],
                article["title"],
                article["description"],
                article["url"],
                article["published_at"],
                article["author"],
                article["category"],
                article["is_politics_related"],
            ),
        )
    if commit:
        connection.commit()


def load_articles(connection: psycopg.Connection, articles: list[Article], commit: bool) -> None:
    for article in articles:
        load_article(connection, article, commit=False)

    if commit:
        connection.commit()
