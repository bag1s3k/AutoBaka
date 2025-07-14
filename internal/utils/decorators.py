import functools
import logging
import time

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
            logger.info(f"Function {func.__name__!r} launching")

            t1 = time.time()
            value = func(*args, **kwargs)

            formate_message = f"| Function: {func.__name__!r} Returned: {str(value)!r} Args/kwargs: {args} | {kwargs} Time: {round(time.time() - t1, 5)}s"

            if not value:
                log_fn = getattr(logger, level.lower(), logger.error)
                log_fn(f"{error_message} {formate_message}")
            else:
                logger.info(f"{right_message} {formate_message}")

            return value

        return wrapper
    return decorator