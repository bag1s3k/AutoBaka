import os
import logging

from dotenv import load_dotenv
from internal.utils.logging_setup import setup_logging
from internal.utils.options import create_agr_parser
from internal.filesystem.paths_constants import ENV_PATH
from internal.utils.var_validator import var_message
from internal.utils.decorators import log_message

setup_logging()
logger = logging.getLogger(__name__)

@log_message("Loading credentials failed", "Loading credentials successfully completed", "critical")
def load_credentials(parser) -> tuple:
    """
    Using argparse load login details
    Returns:
        - tuple: (username, password)
    """

    arg = create_agr_parser(
        parser,
        arg_name=["--login", "-l"],
        nargs=2,
        default=load_credentials_from_file(),
        help_text="enter login details as USERNAME PASSWORD",
        metavar=("USERNAME", "PASSWORD"),
        dest="login_details",
    )

    if not var_message(arg, "arg", "error"):
        return None, None

    return arg.login_details

@log_message("Loading credentials from file failed", "Loading credentials from file successfully completed", "critical")
def load_credentials_from_file() -> tuple:
    """
    Load login details from .env file

    Returns:
        - tuple: (username, password) or (None, None) if failed
    """
    try:
        # Does the file exist
        if not var_message(ENV_PATH.exists(), "ENV_PATH.exist()", "critical", f"ENV path doesn't exist: env path {ENV_PATH}", f"ENV path found env path: {ENV_PATH} "):
            return None, None

        # Loading .env file
        env_loaded = load_dotenv(ENV_PATH)

        if not var_message(env_loaded, "env_loaded", "critical", "env file cannot be loaded", "env file loaded successfully"):
            return None, None

        # Check variables
        def check_env_var(var_name: str) -> str:
            value = os.getenv(var_name)
            var_message(value or value.strip(), "value | value.strip()", "critical", "value not found", "value successfully found")

            return value

        username = check_env_var("BAKA_USERNAME")
        password = check_env_var("BAKA_PASSWORD")

        return username, password

    except Exception as e:
        logger.exception(f"Issue while loading login details: {str(e)}")
        return None, None

@log_message("Set new values failed", "Set new values successfully completed", "error")
def set_env(key: str, value: str) -> bool:
    """
    Set new variables in .env file

    Args:
        key (str): key in .env
        value (str): value in .env that will change

    Returns:
         Bool: True if successful, False otherwise
    """

    lines = []
    found = False

    # Load lines from .env
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        logger.info(f"{ENV_PATH} opened")
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                logger.debug(f"New: {key}={value}")
                found = True
            else:
                lines.append(line)

    if not var_message(found, "found", "error", "Wrong key", "Correct key"):
        return False

    # Set new lines to .env
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        logger.info(f"{ENV_PATH}: opened to set new values")
        f.writelines(lines)

    return True