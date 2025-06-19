from configparser import ConfigParser
from config.logging_conf import setup_logging
from paths import CONFIG_PATH

setup_logging()

def get_config():
    config = ConfigParser()
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config.read_file(f)

    path = config.get("PATHS", "result_path")

    return path