import logging

from configparser import ConfigParser

from internal.utils.logging_setup import setup_logging
from internal.utils.paths_constants import INI_PATH
from pathlib import Path
import configparser

setup_logging()
logger = logging.getLogger(__name__)

def get_config(section: str, option: str):
    """
    Load configuration from the config.ini file

    2 Params:
        - section = enter name of the section
        - option = enter name of the option

    Returns:
        - string
    """
    try:
        logger.debug("Loading configParser")

        # Does the file exist
        if not INI_PATH.exists():
            logger.error(f"Configuration file doesn't exist, wrong path: {INI_PATH}")
            raise FileNotFoundError(f"Configuration file doesn't exist, wrong path: {INI_PATH}")

        config = ConfigParser()

        # Open file config
        with open(INI_PATH, 'r', encoding='utf-8') as f:
            config.read_file(f)

        # Check content of the file config
        if not config.has_section(section):
            logger.error(f"Config file doesn't have [{section}] section")
            raise ValueError(f"Missing [{section}] section")

        if not config.has_option(section, option):
            logger.error(f"In section [{section}] is missing option '{option}'")
            raise ValueError(f"Missing '{option}' in section [{section}]")

        # Get item
        config_item = config.get(section, option)
        logger.debug(f"Config item: {config_item}")

        return config_item

    except Exception as e:
        logger.exception(f"Issue while loading configuration")
        raise e

class IniConfigFile:
    """
    This class represents configuration of the app
    """
    def __init__(self, ini_path: Path):
        logger.debug("Create object that represents config of the app")
        self.ini_path = ini_path

        logger.debug("Create ConfigParser")
        self.config = configparser.ConfigParser()

        logger.info("Read config.ini")
        try:
            self.config.read(ini_path)
            logger.info("config.ini have been successfully read")
        except Exception as e:
            logger.exception(f"Unexpected issue during reading from ini file: {str(e)}")

    def get_config(section: str, option: str):
        """
        Return exactly an element of configuration

        2 Params:
            - section = enter name of the section
            - option = enter name of the option

        Returns:
            - string
        """
        try:
            logger.debug("Loading configParser")

            # Does the file exist
            if not INI_PATH.exists():
                logger.error(f"Configuration file doesn't exist, wrong path: {INI_PATH}")
                raise FileNotFoundError(f"Configuration file doesn't exist, wrong path: {INI_PATH}")

            config = ConfigParser()

            # Open file config
            with open(INI_PATH, 'r', encoding='utf-8') as f:
                config.read_file(f)

            # Check content of the file config
            if not config.has_section(section):
                logger.error(f"Config file doesn't have [{section}] section")
                raise ValueError(f"Missing [{section}] section")

            if not config.has_option(section, option):
                logger.error(f"In section [{section}] is missing option '{option}'")
                raise ValueError(f"Missing '{option}' in section [{section}]")

            # Get item
            config_item = config.get(section, option)
            logger.debug(f"Config item: {config_item}")

            return config_item

        except Exception as e:
            logger.exception(f"Issue while loading configuration")
            raise e