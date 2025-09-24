import logging
from typing import Any
logger = logging.getLogger(__name__)

def log_variable(var: Any, level: str = "error", error_message: str = "Missing or invalid", right_message: str = "Var seems be correct"):
    """
    Function which validates and makes logs

    Args:
        var (any): checking variable
        level (string): invalid logger level
        error_message (string): message which is printed if the variable is invalid
        right_message (string): message which is written into .log file

    Returns:
        var (any): input variable
    """

    if not var:
        log_fn = getattr(logger, level.lower(), logger.error)
        log_fn(error_message)
    else:
        logger.info(right_message)

    return var