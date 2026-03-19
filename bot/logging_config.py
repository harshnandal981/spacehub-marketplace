"""Logging setup utilities for the trading bot."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Mapping


def setup_logging() -> None:
    """Configure file logging for the application."""
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)

    log_file = logs_dir / "app.log"
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if not any(
        isinstance(handler, logging.FileHandler) and Path(handler.baseFilename) == log_file.resolve()
        for handler in root_logger.handlers
    ):
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        root_logger.addHandler(file_handler)


def log_api_request(endpoint: str, payload: Mapping[str, Any]) -> None:
    """Log an outbound API request payload."""
    logging.getLogger(__name__).info("API REQUEST | endpoint=%s | payload=%s", endpoint, payload)


def log_api_response(endpoint: str, response: Mapping[str, Any]) -> None:
    """Log an inbound API response payload."""
    logging.getLogger(__name__).info("API RESPONSE | endpoint=%s | response=%s", endpoint, response)


def log_api_error(endpoint: str, error: Exception) -> None:
    """Log an API-related error message."""
    logging.getLogger(__name__).error("API ERROR | endpoint=%s | error=%s", endpoint, error)


def configure_logging() -> None:
    """Backward-compatible alias for logging setup."""
    setup_logging()
