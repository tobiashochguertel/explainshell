"""Logging configuration using loguru."""

import sys
from pathlib import Path
from typing import Optional

from loguru import logger

from .config import settings


def setup_logging(level: Optional[str] = None, log_file: Optional[Path] = None) -> None:
    """Configure loguru logger.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
    """
    # Remove default handler
    logger.remove()

    # Use provided level or settings
    log_level = level or settings.log_level
    output_file = log_file or settings.log_file

    # Add console handler with rich formatting
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True,
    )

    # Add file handler if specified
    if output_file:
        logger.add(
            output_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
            level=log_level,
            rotation="10 MB",
            retention="1 week",
            compression="gz",
        )

    logger.info(f"Logging initialized at {log_level} level")
