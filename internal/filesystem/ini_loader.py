import logging

from configparser import ConfigParser
from pathlib import Path
from internal.filesystem.paths_constants import INI_PATH
from internal.utils.decorators import message
from internal.utils.var_validator import var_message

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

    @message("Setting new variables failed", "Successfully changed", "warning")
    def set_new(self, section: str, option: str, value: str) -> bool:
        try:

            # Check input (section and option)
            if (
                    not var_message(self.config.has_section(section), "self.config.has_section(section)", "critical", f"No section named {section}", f"Section {section} found")
                    or
                    not var_message(self.config.has_option(section, option), "self.config.has_option(section, option)", "critical", f"No option named {option}", f"Option {option} found")
            ):
                return False

            # Set new
            self.config.set(section, option, value)
            with open(INI_PATH, "w", encoding="utf-8") as f:
                self.config.write(f)

            return True
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return False

    @message("Reading config failed", "Reading config successfully completed", "critical")
    def _read_config(self) -> bool:
        """
        Read config from file

        Returns:
            - bool: True if successful, False otherwise
        """

        try:
            if not var_message(self.ini_path.exists(), "self.ini_path.exist()", "critical", f"Configuration file doesn't exist, path: {self.ini_path}", f"Configuration file found, path: {self.ini_path}"):
                return False

            with open(self.ini_path, "r", encoding="utf-8") as f:
                self.config.read_file(f)

            return True

        except Exception as e:
            logger.exception(f"Unexpected issue during reading from ini file: {str(e)}")
            return False

    @message("Getting config failed", "Config successfully got", "critical")
    def get_config(self, section: str, option: str) -> any:
        """
        Get config element

        Args:
            - section (str): enter name of the section
            - option (str): enter name of the option
        """

        # Check content of the file config
        if (
                not var_message(self.config.has_section(section), "self.config.has_section(section)", "critical",
                                f"No section named {section}", f"Section {section} found")
                or
                not var_message(self.config.has_option(section, option), "self.config.has_option(section, option)",
                                "critical", f"No option named {option}", f"Option {option} found")
        ):
            return False

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
