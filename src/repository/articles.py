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
            published_at,
            text_url,
            image_url,
            summary,
            author_name,
            author_email,
            category,
            is_politics_related
        FROM articles
    """

    params: list[str | bool | int] = []
    conditions = []

    if source:
        conditions.append("source = %s")
        params.append(source)

    if is_politics_related is not None:
        conditions.append("is_politics_related = %s")
        params.append(is_politics_related)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

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
) -> tuple | None:
    query = """
        SELECT
            id,
            source,
            title,
            published_at,
            text_url,
            image_url,
            summary,
            author_name,
            author_email,
            category,
            is_politics_related
        FROM articles
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (article_id,))
        return cursor.fetchone()


def get_article_stats(connection: psycopg.Connection) -> dict:
    query = """
        SELECT
            COUNT(*) AS total_articles,
            COUNT(*) FILTER (
                WHERE is_politics_related = TRUE
            ) AS politics_related
        FROM articles
    """

    source_query = """
        SELECT source, COUNT(*)
        FROM articles
        GROUP BY source
        ORDER BY COUNT(*) DESC
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        total_row = cursor.fetchone()

        cursor.execute(source_query)
        source_rows = cursor.fetchall()

    if total_row is None:
        raise RuntimeError("Failed to fetch article statistics")

    return {
        "total_articles": total_row[0],
        "politics_related": total_row[1],
        "articles_by_source": {row[0]: row[1] for row in source_rows},
    }
