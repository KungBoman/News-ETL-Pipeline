import psycopg
import pytest


@pytest.fixture
def db_connection(monkeypatch):
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5433")
    monkeypatch.setenv("DB_NAME", "news_test")
    monkeypatch.setenv("DB_USER", "news_user")
    monkeypatch.setenv("DB_PASSWORD", "news_password")

    connection = psycopg.connect(
        host="localhost",
        port=5433,
        dbname="news_test",
        user="news_user",
        password="news_password",
    )

    with connection.cursor() as cursor:
        _create_table(cursor)
        _truncate_table(cursor)
        _insert_table(cursor)

    connection.commit()

    yield connection

    with connection.cursor() as cursor:
        _truncate_table(cursor)

    connection.commit()
    connection.close()


def _create_table(cursor):
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


def _truncate_table(cursor):
    cursor.execute("TRUNCATE TABLE articles RESTART IDENTITY")


def _insert_table(cursor):
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
        VALUES
            (
                'SVT',
                'Test article 1',
                'Test description 1',
                'https://example.com/test-1',
                '2026-09-04T10:00:00+00:00',
                NULL,
                NULL,
                FALSE
            ),
            (
                'SVT',
                'Test article 2',
                'Test description 2',
                'https://example.com/test-2',
                '2026-09-04T09:00:00+00:00',
                NULL,
                NULL,
                TRUE
            ),
            (
                'Aftonbladet',
                'Test article 3',
                'Test description 3',
                'https://example.com/test-3',
                '2026-09-04T08:00:00+00:00',
                NULL,
                NULL,
                TRUE
            );
        """
    )
