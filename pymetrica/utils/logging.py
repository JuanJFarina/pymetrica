import sys
import os
from enum import Enum

from loguru import logger

from pydantic import TypeAdapter


class LogLevel(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"


LogLevelAdapter = TypeAdapter(LogLevel)

LOG_LEVEL = os.getenv("PYMETRICA_LOG_LEVEL")
try:
    log_level = LogLevelAdapter.validate_python(LOG_LEVEL)
    logger.info(f"Environment log level set to: {log_level.value}")
except ValueError:
    logger.warning(
        f"Invalid environment log level '{LOG_LEVEL}' provided. Defaulting to 'INFO'.",
    )
    log_level = LogLevel.DEBUG


class CustomLogger:
    def __init__(self) -> None:
        logger.remove()
        self.level = log_level.value
        logger.add(sys.stderr, level=self.level)
        self.logger = logger

    def info(self, message: str) -> None:
        self.logger.info(message)

    def warning(self, message: str) -> None:
        self.logger.warning(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)


log: CustomLogger = CustomLogger()

log.info(f"Pymetrica logging initialized with level: {log.level}")
