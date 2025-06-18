import os
from dotenv import load_dotenv
from config.logging_conf import setup_logging

setup_logging()

def load_credentials():
    load_dotenv()
    username = os.getenv("BAKA_USERNAME")
    password = os.getenv("BAKA_PASSWORD")

    return username, password