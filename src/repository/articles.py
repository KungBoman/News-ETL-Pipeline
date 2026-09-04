import psycopg


def get_articles(
    connection: psycopg.Connection,
    limit: int,
    offset: int,
    source: str | None = None,
    is_politics_related: bool | None = None,
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
    """

    params = []

    if source:
        query += " WHERE source = %s"
        params.append(source)

    if is_politics_related:
        query += " WHERE is_politics_related = %s"
        params.append(is_politics_related)

    query += """
        ORDER BY published_at DESC
        LIMIT %s
        OFFSET %s
    """

    params.extend([limit, offset])

    with connection.cursor() as cursor:
        cursor.execute(query, params)
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
