import functools
import logging
import sys
from typing import Any

logger = logging.getLogger(__name__)


def validate_output(
        error_msg: str = "Something went wrong",
        success_msg: str = "",
        level: str = "error",
        allow_empty=False):
    """ Decorator that logs a message depending on the return value of the decorated function.
        - If the function returns a falsy value (e.g. None, False, empty string),
          an error message is logged.
        - If the function returns a truthy value, a success message is logged.
        :param error_msg: Message to log if the decorated function returns a falsy value.
        :param success_msg: Message to log if the decorated function returns a truthy value.
        :param level: Logging level to use when the decorated function returns a falsy value
                 (e.g. "error", "warning", "info"). Defaults to "error".
        :param allow_empty: output can be empty
        :return Any: The original return value of the decorated function.

        Example:
            >>> @validate_output(error_msg="Login failed", success_msg="Login successful", level="error")
            ... def login(user, password):
            ...     return user == "admin" and password == "secret"
            >>> login("correct", "wrong")
            # logs: "Login failed" (error)
            False"""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            if not result and not allow_empty:
                # getattr instead writing if statements for each logger level
                logger_method = getattr(logger, level.lower(), logger.error)
                logger_method(error_msg)
                if level.lower() in ["critical"]:
                    sys.exit(-1)
            else:
                if success_msg:
                    logger.info(success_msg)

            return result

        return wrapper

    return decorator