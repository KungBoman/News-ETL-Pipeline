import logging
from typing import ClassVar


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.INFO: "\033[37m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[35m",
    }

    RESET: ClassVar[str] = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        levelname = f"{color}{record.levelname}{self.RESET}"

        return (
            f"{self.formatTime(record)} - "
            f"{levelname} - "
            f"{record.name} - "
            f"{record.getMessage()}"
        )


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            ColorFormatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
        )

        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger
