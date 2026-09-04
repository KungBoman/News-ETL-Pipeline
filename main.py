import psycopg

from src.logger import get_logger
from src.pipeline import run_pipeline

logger = get_logger(__name__)


def main() -> None:
    try:
        stats = run_pipeline()

        logger.info(f"Extracted: {stats['extracted']} articles")
        logger.info(f"Transformed: {stats['transformed']} articles")
        logger.info(f"Valid: {stats['valid']} articles")
        logger.info(f"Loaded: {stats['loaded']} articles")

    except psycopg.OperationalError as error:
        logger.error(f"Database connection failed: {error}")
        raise SystemExit(1)

    except KeyboardInterrupt:
        logger.info("Quitting...")


if __name__ == "__main__":
    main()
