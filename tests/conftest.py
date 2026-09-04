import psycopg
import pytest


@pytest.fixture
def db_connection():
    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="news_test",
        user="news_user",
        password="news_password",
    )

    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS articles (
                id SERIAL PRIMARY KEY,
                source TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                url TEXT UNIQUE NOT NULL,
                published_at TIMESTAMPTZ NOT NULL,
                author TEXT,
                category TEXT,
                is_politics_related BOOLEAN NOT NULL
            );
            """
        )

        cursor.execute(
            """
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
                'SVT',
                'Test article',
                'Test description',
                'https://example.com/test',
                '2026-09-04T10:00:00+00:00',
                NULL,
                NULL,
                FALSE
            );
            """
        )

    connection.commit()

    yield connection

    with connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE articles RESTART IDENTITY")

    connection.commit()
    connection.close()
