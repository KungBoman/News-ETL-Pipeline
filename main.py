import time

import psycopg

from src.logger import get_logger
from src.pipeline import run_pipeline

logger = get_logger(__name__)


def main() -> None:
    start_time = time.perf_counter()
    logger.info("=== Pipeline started ===")

    try:
        stats = run_pipeline()

        duration = time.perf_counter() - start_time

        logger.info(f"Extracted: {stats['extracted']} articles")
        logger.info(f"Transformed: {stats['transformed']} articles")
        logger.info(f"Valid: {stats['valid']} articles")
        logger.info(f"Loaded: {stats['loaded']} articles")
        logger.info(f"=== Pipeline completed in {duration:.2f}s ===")

    except psycopg.OperationalError as error:
        logger.error(f"Database connection failed: {error}")
        raise SystemExit(1)

    except KeyboardInterrupt:
        logger.info("Quitting...")


if __name__ == "__main__":
    main()
