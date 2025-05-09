import logging
from datetime import datetime


def setup_logger(
    name: str = "app_logger",
    log_file: str = "application.log",
    level: int = logging.INFO,
    fmt: str = "%(asctime)s | %(levelname)s | %(message)s",
    to_console: bool = True,
    to_file: bool = True,
) -> logging.Logger:
    """
    logger_utils.py — Reusable logging setup utility

    Provides a configurable `setup_logger()` function to easily create loggers that
    write to both console and file with timestamped, leveled messages.

    Usage Example:
    --------------
    from logger_utils import setup_logger

    logger = setup_logger(
        name="my_script",
        log_file="my_script.log",
        level=logging.DEBUG
    )

    logger.info("Processing started")
    logger.warning("Found something unusual at index %d", index)
    try:
     ...
    except Exception as e:
        logger.error("An error occurred: %s", str(e))

    Parameters:
    -----------
    name : str
        The name of the logger instance. Useful for filtering or nested modules.
    log_file : str
        File path to write log output to (only used if to_file=True).
    level : int
        Logging level, e.g., logging.INFO, logging.DEBUG, etc.
    fmt : str
        Format string for log output. Defaults to timestamp | level | message.
    to_console : bool
        If True, logs will be shown in the terminal/console.
    to_file : bool
        If True, logs will be written to the specified file.

    Returns:
    --------
    logging.Logger
        A configured logger instance ready for use.
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter(fmt)

    if to_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    if to_console:
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    return logger
