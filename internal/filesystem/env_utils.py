import os
import logging

from dotenv import load_dotenv
from internal.utils.logging_setup import setup_logging
from internal.utils.arg_parser import create_agr_parser
from paths_constants import PATHS
from internal.utils.decorators import validate_output

setup_logging()
logger = logging.getLogger(__name__)


@validate_output(
    error_msg="Loading credentials failed",
    success_msg="Loading credentials successful",
    level="error"
)
def load_credentials(parser) -> tuple:
    """Using argparse load login details
         - default option is load credentials from file
        :return arg.login_details:  (username, password)"""
    arg = create_agr_parser(
        parser,
        arg_name=["--login", "-l"],
        nargs=2,
        default=load_credentials_from_file(),
        help_text="Enter login details in form USERNAME PASSWORD e.g. python main.py -l username password",
        metavar=("USERNAME", "PASSWORD"),
        dest="login_details",
    )
    
    if not arg:
        logger.error("Retrieving credentials failed")
        return None, None

    return arg.login_details


@validate_output(
    error_msg="Retrieving credentials from file failed",
    success_msg="Loading credentials from file successful",
    level="error"
)
def load_credentials_from_file() -> tuple:
    """Loading login details from .env file
        :return: username, password: (username, password) or (None, None) if failed"""

    if not load_dotenv(PATHS.env):
        logger.error("env file cannot be loaded")
        return None, None

    # Check variables
    def check_env_var(var_name: str) -> str:
        value = os.getenv(var_name)
        if not value or not value.strip():
            logger.error("Username or password not found in .env")

        return value

    username = check_env_var("BAKA_USERNAME")
    password = check_env_var("BAKA_PASSWORD")

    return username, password