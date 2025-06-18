from configparser import ConfigParser
from config.logging_conf import setup_logging

setup_logging()

def get_config():
    config = ConfigParser()
    with open('config.ini', 'r', encoding='utf-8') as f:
        config.read_file(f)

    path = config.get("PATHS", "result_path")

    return path