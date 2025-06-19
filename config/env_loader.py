import os
import logging

from dotenv import load_dotenv
from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def load_credentials() -> tuple:
    """
    Load login details
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