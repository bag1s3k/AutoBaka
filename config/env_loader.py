import os
import logging

from dotenv import load_dotenv
from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def load_credentials():
    """
        
    """
    load_dotenv()
    username = os.getenv("BAKA_USERNAME")
    password = os.getenv("BAKA_PASSWORD")

    return username, password