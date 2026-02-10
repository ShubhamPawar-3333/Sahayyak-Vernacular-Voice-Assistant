"""Sahayyak - Vernacular Voice Assistant for Maharashtra Government Services."""

__version__ = "0.1.0"

from app.config import get_config
from app.logging_config import get_logger, setup_logging

__all__ = ["get_config", "get_logger", "setup_logging"]
