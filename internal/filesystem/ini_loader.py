import logging

from configparser import ConfigParser
from internal.utils.logging_setup import setup_logging
from pathlib import Path
from internal.filesystem.paths_constants import INI_PATH

setup_logging()
logger = logging.getLogger(__name__)

class IniConfigFile:
    """
    This class represents configuration of the app
    """
    def __init__(self, ini_path: Path):
        """
        Init method of IniConfigFile

        Args:
            - ini_path (Path): path of ini file location
        """
        logger.debug("Create object that represents config of the app")

        self.ini_path = ini_path
        self.config = ConfigParser()
        self.read = self._read_config()

    def set_new(self, section: str, option: str, value: str) -> bool:
        try:
            if not self.config.has_section(section):
                logger.error(f"No section: {section}")
                return False
            if not self.config.has_option(section, option):
                logger.error(f"No option: {section} {option}")
                return False

            self.config.set(section, option, value)
            with open(INI_PATH, "w", encoding="utf-8") as f:
                self.config.write(f)

            logger.info("Successfully changed")

            return True
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return False

    def _read_config(self) -> bool:
        """
        Read config from file

        Returns:
            - bool: True if successful, False otherwise
        """

        logger.info("Read config.ini")

        try:
            if not self.ini_path.exists():
                logger.exception(f"Configuration file doesn't exist, wrong path: {self.ini_path}")
                return False

            with open(self.ini_path, "r", encoding="utf-8") as f:
                self.config.read_file(f)

            logger.info("config.ini have been successfully read")

            return True

        except Exception as e:
            logger.exception(f"Unexpected issue during reading from ini file: {str(e)}")
            return False

    def get_config(self, section: str, option: str):
        """
        Get config element

        Args:
            - section (str): enter name of the section
            - option (str): enter name of the option
        """

        # Check content of the file config
        if not self.config.has_section(section):
            logger.error(f"Config file doesn't have [{section}] section")
            raise ValueError(f"Missing [{section}] section")

        if not self.config.has_option(section, option):
            logger.error(f"In section [{section}] is missing option '{option}'")
            raise ValueError(f"Missing '{option}' in section [{section}]")

        config_item = self.config.get(section, option)
        logger.debug(f"Config item: {config_item}")

        return self._auto_cast(config_item)

    @staticmethod
    def _auto_cast(value: str):
        """
        Try to convert string to int, bool or keep as str

        Args:
            value (str): value from config file

        Returns:
            Union[int, bool, str]: best-match
        """

        if value in ["True", "False"]:
            return True if value == "True" else False

        elif value.isdigit():
            return int(value)

        else:
            return value


config = IniConfigFile(INI_PATH)
