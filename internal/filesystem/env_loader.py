import os
import logging
import time

from dotenv import load_dotenv
from internal.utils.logging_setup import setup_logging
from internal.utils.options import get_args
from internal.filesystem.paths_constants import ENV_PATH

setup_logging()
logger = logging.getLogger(__name__)

def load_credentials() -> tuple:
    """
    Using argparse chose login details from file or from user
    Returns:
        - tuple: (username, password)
    """

    args = get_args() # Get argparse options

    # User or file
    if args.user:
        logger.info("Selected user option")
        return load_credentials_from_user()
    elif args.file:
        logger.info("Selected file option")
        return load_credentials_from_file()
    else:
        logger.warning("Default option")
        return load_credentials_from_file() # Default option is from file

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

def load_credentials_from_user() -> tuple:
    """
    Load login details from user input

    Returns:
        - tuple: (username, password) or (None, None) if failed
    """
    try:
        logger.info("Loading login details from user input")
        time.sleep(3)
        details = input("Enter login details in form: username, password\n> ").split(", ")

        return tuple(x.strip() for x in details)

    except Exception as e:
        logger.exception(f"Error during user input: {str(e)}")
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
        for line in f:
            if line.startswith(f"{key}="):
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)
    if not found:
        logger.error(f"Write to {ENV_PATH} failed, wrong key")
        return False

    # Set new lines to .env
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return True