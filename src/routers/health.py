from fastapi import APIRouter

from src.load import try_create_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    connection = try_create_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return {
            "status": "ok",
            "database": "ok",
        }

    finally:
        connection.close()
