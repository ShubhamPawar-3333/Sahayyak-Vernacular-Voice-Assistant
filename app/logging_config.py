"""
Logging configuration for Sahayyak Voice Assistant.
Provides structured logging with JSON format for production.
"""

import logging
import sys
from typing import Optional

from app.config import get_config


def setup_logging(level: Optional[str] = None) -> logging.Logger:
    """
    Configure and return the application logger.

    Args:
        level: Log level override. If None, uses config value.

    Returns:
        Configured logger instance.
    """
    config = get_config()
    log_level = level or config.app.log_level

    # Create logger
    logger = logging.getLogger("sahayyak")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler with formatting
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Format based on environment
    if config.app.is_production:
        # JSON format for production (easier to parse in logs)
        formatter = logging.Formatter(
            '{"time": "%(asctime)s", "level": "%(levelname)s", '
            '"module": "%(module)s", "message": "%(message)s"}'
        )
    else:
        # Human-readable for development
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s",
            datefmt="%H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name suffix. If None, returns root app logger.

    Returns:
        Logger instance.
    """
    if name:
        return logging.getLogger(f"sahayyak.{name}")
    return logging.getLogger("sahayyak")
