import logging
import sys
from typing import Optional


def setup_logger(level: str = "INFO", log_file: Optional[str] = None):
    """Configure logging for the game."""
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))

    # Create formatters
    console_formatter = logging.Formatter("%(levelname)s: %(message)s")
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Suppress prometheus_client logs unless they're errors
    logging.getLogger("prometheus_client").setLevel(logging.ERROR)
