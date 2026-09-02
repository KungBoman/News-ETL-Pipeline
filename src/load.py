import psycopg


def create_connection():
    return psycopg.connect(
        host="localhost",
        port=5432,
        dbname="news",
        user="news_user",
        password="news_password",
    )


def load_article(connection, article):
    pass


def load_articles(connection, articles):
    pass
