import logging
from pathlib import Path

from helpers.date_time_helper import DateTimeHelper


class ReadableTimeFormatter(logging.Formatter):
    """Custom formatter that uses readable datetimes."""

    def formatTime(self, record, datefmt=None):
        return DateTimeHelper.get_readable_datetime(record.created)


class LogHelper:
    """Centralized logger helper with flexible output options."""

    _logger = None

    @staticmethod
    def get_logger(
        name: str = "AppLogger",
        log_to: str = "stdout",  # 'stdout', 'file', or 'both'
        log_file: str = "app.log",
        log_dir: str = "logs",
        level: int = logging.INFO,
    ) -> logging.Logger:
        """Returns a configured singleton logger."""
        if LogHelper._logger:
            return LogHelper._logger

        logger = LogHelper._create_logger(name, level)
        formatter = LogHelper._create_formatter()

        handlers = LogHelper._create_handlers(log_to, formatter, log_dir, log_file)
        for handler in handlers:
            logger.addHandler(handler)

        LogHelper._logger = logger
        return logger

    # --- Internal helper methods ---

    @staticmethod
    def _create_logger(name: str, level: int) -> logging.Logger:
        """Creates the base logger."""
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False
        return logger

    @staticmethod
    def _create_formatter() -> logging.Formatter:
        """Creates and returns the custom readable-time formatter."""
        return ReadableTimeFormatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

    @staticmethod
    def _create_handlers(
        log_to: str, formatter: logging.Formatter, log_dir: str, log_file: str
    ) -> list[logging.Handler]:
        """Creates handlers based on where to log (stdout, file, both)."""
        handlers = []

        if log_to in ("stdout", "both"):
            handlers.append(LogHelper._create_stream_handler(formatter))

        if log_to in ("file", "both"):
            handlers.append(LogHelper._create_file_handler(formatter, log_dir, log_file))

        return handlers

    @staticmethod
    def _create_stream_handler(formatter: logging.Formatter) -> logging.StreamHandler:
        """Creates a stream handler (stdout)."""
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def _create_file_handler(
        formatter: logging.Formatter, log_dir: str, log_file: str
    ) -> logging.FileHandler:
        """Creates a file handler (with automatic directory creation)."""
        Path(log_dir).mkdir(exist_ok=True)
        file_path = Path(log_dir) / log_file
        handler = logging.FileHandler(file_path, encoding="utf-8")
        handler.setFormatter(formatter)
        return handler