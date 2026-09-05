from datetime import datetime

import psycopg


def create_pipeline_run(
    connection: psycopg.Connection,
    started_at: datetime,
) -> int:
    query = """
        INSERT INTO pipeline_runs (started_at, status)
        VALUES (%s, %s)
        RETURNING id
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (started_at, "running"))
        result = cursor.fetchone()

    if result is None:
        raise RuntimeError("Failed to create pipeline run")

    connection.commit()

    return result[0]


def finish_pipeline_run(
    connection: psycopg.Connection,
    run_id: int,
    finished_at: datetime,
    status: str,
    extracted: int | None,
    transformed: int | None,
    valid: int | None,
    loaded: int | None,
    error: str | None = None,
) -> None:
    query = """
        UPDATE pipeline_runs
        SET
            finished_at = %s,
            status = %s,
            extracted = %s,
            transformed = %s,
            valid = %s,
            loaded = %s,
            error = %s
        WHERE id = %s
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (
                finished_at,
                status,
                extracted,
                transformed,
                valid,
                loaded,
                error,
                run_id,
            ),
        )

    connection.commit()


def get_pipeline_runs(
    connection: psycopg.Connection,
    limit: int,
    offset: int,
) -> list[tuple]:
    query = """
        SELECT
            id,
            started_at,
            finished_at,
            status,
            extracted,
            transformed,
            valid,
            loaded,
            error
        FROM pipeline_runs
        ORDER BY started_at DESC
        LIMIT %s
        OFFSET %s
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (limit, offset))
        return cursor.fetchall()
