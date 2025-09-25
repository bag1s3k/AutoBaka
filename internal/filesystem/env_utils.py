import os
import logging

from dotenv import load_dotenv
from internal.utils.logging_setup import setup_logging
from internal.utils.arg_parser import create_agr_parser
from internal.filesystem.paths_constants import ENV_PATH
from internal.utils.var_validator import log_variable
from internal.utils.decorators import log_message

setup_logging()
logger = logging.getLogger(__name__)


@log_message(error_message="Loading credentials failed",
             right_message="Loading credentials successfully completed",
             level="critical")
def load_credentials(parser) -> tuple:
    """
    Using argparse load login details
    (default option is load credentials from file)

    :return arg.login_details:  (username, password)
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

    if not log_variable(arg, "critical", "Retrieving credentials failed"):
        return None, None

    return arg.login_details


@log_message(error_message="Retrieving credentials from file failed",
             right_message="Loading credentials from file successful",
             level="critical")
def load_credentials_from_file() -> tuple:
    """
    Loading login details from .env file

    :return: username, password: (username, password) or (None, None) if failed
    """
    try:
        # Does the file exist
        if not log_variable(ENV_PATH.exists(),
                            level="critical",
                            error_message=f"ENV path doesn't exist: env path {ENV_PATH}",
                            right_message="ENV path found"):
            return None, None

        # Loading .env file
        env_loaded = load_dotenv(ENV_PATH)

        if not log_variable(env_loaded,
                            level= "critical",
                            error_message="env file cannot be loaded",
                            right_message="env file loaded successfully"):
            return None, None

        # Check variables
        def check_env_var(var_name: str) -> str:
            value = os.getenv(var_name)
            log_variable(value or value.strip(), "critical", "Username or password not found in .env")

            return value

        username = check_env_var("BAKA_USERNAME")
        password = check_env_var("BAKA_PASSWORD")

        return username, password

    except Exception as e:
        logger.exception(f"Issue while loading login details: {str(e)}")
        return None, None