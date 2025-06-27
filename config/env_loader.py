import os
import logging
import time

from dotenv import load_dotenv
from config.logging_conf import setup_logging
from config.options import get_args

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
    Load login details from file
        - tuple: (username, password)
    """
    try:
        logger.info("Loading login details from .env file")

        # Loading .env file
        env_loaded = load_dotenv()

        if not env_loaded:
            logger.warning(".env file cannot be load")
        else:
            logger.info(".env file was successfully loaded")

        # Check variables
        def check_env(var_name) -> str:
            value = os.getenv(var_name)
            if not value or not value.strip():
                logger.error(f"Variable is not set or it's empty")
            if value:
                logger.debug("Login details loaded successfully")
            return value

        username = check_env("BAKA_USERNAME")
        password = check_env("BAKA_PASSWORD")

        return username, password

    except Exception as e:
        logger.exception(f"Issue while loading login details: {str(e)}")
        return None, None

def load_credentials_from_user() -> tuple:
    """
    Load login details from console
    Returns:
        - tuple: (username, password)
    """
    try:
        logger.info("Loading login details from cmd")
        time.sleep(3)
        details = input("Enter login details in form: username, password\n> ").split(", ")

        return tuple(x.strip() for x in details)
    except Exception as e:
        logger.exception(f"Issue while loading login details from console: {str(e)}")
        return None, None