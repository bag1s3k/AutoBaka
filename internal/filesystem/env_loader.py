import os
import logging
import time

from click import argument
from dotenv import load_dotenv
from internal.utils.logging_setup import setup_logging
from internal.utils.options import create_agr_parser
from internal.filesystem.paths_constants import ENV_PATH

setup_logging()
logger = logging.getLogger(__name__)

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

    if not arg:
        logger.error("arg is None")
        return None, None

    logger.info("successfully returned login details")
    return arg.login_details

def load_credentials_from_file() -> tuple:
    """
    Load login details from .env file

    Returns:
        - tuple: (username, password) or (None, None) if failed
    """
    try:
        logger.info("Loading login details from .env file")

        # Does the file exist
        if not ENV_PATH.exists():
            logger.error(f".env file not found at: {ENV_PATH}")
            return None, None

        # Loading .env file
        env_loaded = load_dotenv(ENV_PATH)

        if not env_loaded:
            logger.warning(".env file cannot be load")
            return None, None

        logger.info(".env file was successfully loaded")

        # Check variables
        def check_env_var(var_name: str) -> str:
            value = os.getenv(var_name)
            if not value or not value.strip():
                logger.error(f"Variable is not set or empty")
            if value:
                logger.debug("Login details loaded successfully")
            return value

        username = check_env_var("BAKA_USERNAME")
        password = check_env_var("BAKA_PASSWORD")

        return username, password

    except Exception as e:
        logger.exception(f"Issue while loading login details: {str(e)}")
        return None, None

def set_env(key: str, value: str) -> bool:
    """
    Set new variables in .env file

    Args:
        key (str): key in .env
        value (str): value in .env which is gonna be change

    Returns:
         Bool: True if successful, False otherwise
    """

    logger.info(f"Changing variables in {ENV_PATH}")
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

    if not found:
        logger.error(f"Write to {ENV_PATH} failed, wrong key")
        return False

    # Set new lines to .env
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        logger.info(f"{ENV_PATH}: opened to set new values")
        f.writelines(lines)

    return True