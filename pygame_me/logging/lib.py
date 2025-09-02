"""Internals for logging setup."""

import multiprocessing
from pathlib import Path

from structlog.dev import DIM, RESET_ALL
from structlog.types import EventDict, WrappedLogger


def convert_paths(_logger: WrappedLogger, _method_name: str, event_dict: EventDict) -> EventDict:
    """Convert any Path fields to strings."""
    for key, value in event_dict.items():
        if isinstance(value, Path):
            event_dict[key] = str(value)
    return event_dict


def strip_logger_if_main(_logger: WrappedLogger, _method_name: str, event_dict: EventDict) -> EventDict:
    """Remove the logger field if it's just __main__."""
    if event_dict.get("logger", None) == "__main__":
        event_dict.pop("logger")
    return event_dict


def add_process_name(_logger: WrappedLogger, method_name: str, event_dict: EventDict) -> EventDict:
    """Add process name for subprocesses.

    LogRecords have this anyway, but this way structlog renderers print it.
    """
    process_name = multiprocessing.current_process().name
    if process_name != "MainProcess":
        event_dict["process_name"] = process_name
    return event_dict


def make_debug_messages_dim(_logger: WrappedLogger, _method_name: str, event_dict: EventDict) -> EventDict:
    """Dim Debug messages."""
    if event_dict["level"] == "debug":
        # HACK: overrule ConsoleRenderer's formatting to de-emphasize this bit
        event_dict["event"] = RESET_ALL + DIM + event_dict["event"] + RESET_ALL
    return event_dict
