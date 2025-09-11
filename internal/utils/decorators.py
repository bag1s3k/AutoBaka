import functools
import logging
from typing import Any

logger = logging.getLogger(__name__)

def log_message(error_message: str = "Function failed", right_message: str = "Function successful", level: str = "error"):
    """
    Decorator that logs a message depending on the return value of the decorated function.

    - If the function returns a falsy value (e.g. None, False, empty string),
      an error message is logged.
    - If the function returns a truthy value, a success message is logged.

    Args:
        error_message (str): Message to log if the decorated function returns a falsy value.
        right_message (str): Message to log if the decorated function returns a truthy value.
        level (str): Logging level to use when the decorated function returns a falsy value
                     (e.g. "error", "warning", "info"). Defaults to "error".

    Returns:
        Any: The original return value of the decorated function.

    Example:
        >>> @log_message(error_message="Login failed", right_message="Login successful", level="critical")
        ... def login(user, password):
        ...     return user == "admin" and password == "secret"
        >>> login("correct", "wrong")
        # logs: "Login failed" (CRITICAL)
        False
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            if not result:
                logger_method = getattr(logger, level.lower(), logger.error) # getattr instead writing if statements for each logger level
                logger_method(error_message)
            else:
                logger.info(right_message)

            return result

        return wrapper

    return decorator