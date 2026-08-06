"""
Unified logging module for AeroTwin.

Provides:
  - setup_logging()  — called once during application lifespan startup

Design decision: all logging configuration is consolidated here rather than
splitting across core/ and shared/logging/. This maximises locality.
"""

from __future__ import annotations

import logging
import sys

import structlog

from app.config.settings import settings


def setup_logging() -> None:
    """
    Configure structlog for the application.

    - Development / testing: coloured ConsoleRenderer for human readability.
    - Production: JSON renderer for log aggregation (Datadog, Elastic, etc.).

    Must be called once during the lifespan startup before any log is emitted.
    """
    shared_processors: list[structlog.types.Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.ENVIRONMENT == "production":
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer(colors=True)

    structlog.configure(
        processors=shared_processors + [renderer],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Route stdlib logging through structlog so third-party libs appear in the
    # same stream.
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
    )
