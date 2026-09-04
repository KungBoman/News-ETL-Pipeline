import psycopg


def get_articles(
    connection: psycopg.Connection,
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
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        return cursor.fetchall()
