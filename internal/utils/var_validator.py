import logging

logger = logging.getLogger(__name__)

def var_message(var: any, var_name: str, level: str = "error", error_message: str = "Missing or invalid", right_message: str = "Correct"):
    """
    Function which validates and makes logs

    Args:
        var (any): checking variable
        var_name (string): name of the checking variable
        level (string): invalid logger level
        error_message (string): message which is printed if the variable is invalid
        right_message (string): message which is written into .log file

    Returns:
        var (any): input variable
    """

    formate_message = f"Variable: {var_name!r} | {var} | {type(var)}" # formate output of the variable status

    if not var:
        log_fn = getattr(logger, level.lower(), logger.error)
        log_fn(f"{error_message}: {formate_message}")
    else:
        logger.info(f"{right_message}: {formate_message}")

    return var