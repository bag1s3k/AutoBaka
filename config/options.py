import argparse
import logging

from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def get_args():
    """
    Setup options
        - --user = enter login details manually
        - --file = default option, login details from file
    """

    # Config ArgParse
    logger.info("Config argparse")
    parser = argparse.ArgumentParser()
    parser.add_argument("--user", action="store_true")
    parser.add_argument("--file", action="store_true")

    return parser.parse_args()