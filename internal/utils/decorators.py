import functools
import logging

from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def message(error_message: str = "Function failed", right_message: str = "Function successful", level: str = "error"):
    """
    Decorator that logs a message base on the return value of the decorator function

    Args:
        error_message (str): Message to log if the function returns falsy value
        right_message (str): Message to log if the function returns truthy value
        level (str): Message to log if the function returns falsy value

    Returns:
         value: value which is returned by func
    """
    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"{func.__name__} started")

            value = func(*args, **kwargs)

            if not value:
                log_fn = getattr(logger, level.lower(), logger.error)
                log_fn(error_message)
            else:
                logger.info(right_message)

            return value

        return wrapper
    return decorator