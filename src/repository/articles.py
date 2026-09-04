import psycopg


def get_articles(
    connection: psycopg.Connection,
    limit: int,
    offset: int,
) -> list[tuple]:
    query = """
        SELECT
            id,
            source,
            title,
            description,
            url,
            published_at,
            author,
            category,
            is_politics_related
        FROM articles
        ORDER BY published_at DESC
        LIMIT %s
        OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()


def get_article_by_id(
    connection: psycopg.Connection,
    article_id: int,
) -> list[tuple]:
    query = """
        SELECT
            id,
            source,
            title,
            description,
            url,
            published_at,
            author,
            category,
            is_politics_related
        FROM articles
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (article_id,))
        return cursor.fetchone()
