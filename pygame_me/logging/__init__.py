"""Set up Logging."""

import logging
from enum import Enum

import structlog
import structlog_round

from pygame_me.logging import lib

# TODO: Change loglevel

get_logger = structlog.get_logger


class LogLevel(str, Enum):
    """Represents the available log levels."""

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"
    DEBUG = "DEBUG"
    NOTSET = "NOTSET"


# root_logger = logging.getLogger()
# root_logger.setLevel(LogLevel.DEBUG.value)

logging.basicConfig(
    format="%(message)s",
    # stream=sys.stdout,
    level=logging.DEBUG,
)

DIM, RESET_ALL = structlog.dev.DIM, structlog.dev.RESET_ALL


class DimDebugRenderer(structlog.dev.ConsoleRenderer):
    """Additionally dim debug log messages."""

    def __call__(self, logger, name, event_dict):
        rendered = super().__call__(logger, name, event_dict)
        if event_dict.get("level") == "debug":
            return f"{DIM}{rendered}{RESET_ALL}"
        return rendered


level_styles = structlog.dev.ConsoleRenderer.get_default_level_styles()
level_styles["debug"] = structlog.dev.DIM

structlog.configure(
    processors=[
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        lib.strip_logger_if_main,
        structlog_round.FloatRounder(digits=3),
        lib.add_process_name,
        lib.convert_paths,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        # structlog.processors.TimeStamper(fmt="%H:%M:%S", utc=False),
        # lib.make_debug_messages_dim,
        DimDebugRenderer(pad_event=60, sort_keys=False, level_styles=level_styles),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(LogLevel.DEBUG),
    logger_factory=structlog.stdlib.LoggerFactory(),
)
log = structlog.get_logger()

# import logging
# import sys
# from typing import ClassVar


# class CustomFormatter(logging.Formatter):
#     """Custom formatter for colored log messages.

#     This class extends the logging.Formatter class to provide
#     colored log messages based on their severity level.
#     """

#     grey = "\x1b[38;20m"
#     yellow = "\x1b[33;20m"
#     red = "\x1b[31;20m"
#     bold_red = "\x1b[31;1m"
#     reset = "\x1b[0m"
#     message = "%(levelname)s: %(message)s"

#     FORMATS: ClassVar[dict[int, str]] = {
#         logging.DEBUG: grey + message + reset,
#         logging.INFO: grey + message + reset,
#         logging.WARNING: yellow + message + reset,
#         logging.ERROR: red + message + reset,
#         logging.CRITICAL: bold_red + message + reset,
#     }

#     def format(self, record: logging.LogRecord) -> str:
#         """Format the log record."""
#         log_fmt = self.FORMATS.get(record.levelno)
#         formatter = logging.Formatter(log_fmt)
#         return formatter.format(record)


# # If you want to be spammed less choose a different logging level:
# # DEBUG
# # INFO
# # WARNING
# # ERROR
# # CRITICAL


# def setup_logging(log_level: int | LogLevel) -> None:
#     """Initialise logger."""
#     # Setting root logger is bad practise, too bad!
#     logger = logging.root
#     logger.setLevel(log_level)
#     # create console handler with a higher log level
#     ch = logging.StreamHandler()
#     ch.setLevel(log_level)
#     ch.setFormatter(CustomFormatter())
#     logger.addHandler(ch)

# LEVELS = {
#     "DEBUG": 10,
#     "INFO": 20,
#     "WARNING": 30,
#     "ERROR": 40,
#     "CRITICAL": 50,
# }

# args = sys.argv
# try:
#     arg = sys.argv[1]
#     if not (LOG_LEVEL := LEVELS.get(arg)):
#         LOG_LEVEL = int(sys.argv[1])
# except (IndexError, ValueError):
#     LOG_LEVEL = 20
