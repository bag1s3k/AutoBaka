import logging
from typing import Any
logger = logging.getLogger(__name__)


def log_variable(var: Any, level: str = "error", error_msg: str = "Missing or invalid", success_msg: str = "Var seems be correct"):

    """
    Function which validates and makes logs
    :param var: checking variable
    :param level: invalid logger level
    :param error_msg: message which is printed if the variable is invalid
    :param success_msg: message which is written into .log file
    :return var: input variable
    """

    if not var:
        log_fn = getattr(logger, level.lower(), logger.error)
        log_fn(error_msg)
    else:
        logger.info(success_msg)

    return var