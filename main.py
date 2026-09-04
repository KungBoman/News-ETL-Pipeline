import psycopg

from src.logger import get_logger
from src.pipeline import run_pipeline

logger = get_logger(__name__)


def main() -> None:
    try:
        stats = run_pipeline()

        print(f"Extracted: {stats['extracted']} articles")
        print(f"Transformed: {stats['transformed']} articles")
        print(f"Valid: {stats['valid']} articles")
        print(f"Loaded: {stats['loaded']} articles")

    except psycopg.OperationalError as error:
        print(f"Database connection failed: {error}")
        raise SystemExit(1)

    except KeyboardInterrupt:
        logger.info("Quitting...")


if __name__ == "__main__":
    main()
