import functools
import logging
import sys
from pathlib import Path
from typing import Any
from time import time

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
                 (e.g. "error", "warning", "info"). Defaults to "error". To exit the program use 'critical'
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

            def execute():
                """ Show logger or exit the program """

                # getattr instead writing if statements for each logger level
                logger_method = getattr(logger, level.lower(), logger.error)
                logger_method(error_msg)
                if level.lower() in ["critical"]:
                    sys.exit(-1)

            if not result and not allow_empty:
                execute()
            elif isinstance(result, Path) and not result.exists():
                execute()
            else:
                if success_msg:
                    logger.info(success_msg)

            return result

        return wrapper

    return decorator


def timer(func):
    """It shows the execution time of the function object passed"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        t1 = time()
        result = func(*args, **kwargs)
        print(f"Function {func.__name__!r} executed in {(time() - t1):.2f}s")

        return result

    return wrapper