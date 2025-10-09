import logging
import configparser

from internal.filesystem.paths_constants import INI_PATH
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class AutoCastConfigParser(configparser.ConfigParser):
    def get_auto_cast(self, section, option):
        """Try to convert string to int, bool or keep it as str
            - override .get
            :param section: name of the section
            :param option: name of the option
            :return Union[int, bool, str]: best-match"""
        try:
            value = super().get(section, option)
        except Exception as e:
            logger.exception(e)
            return None

        if value in ["True", "False"]:
            return True if value == "True" else False
        elif value.isdigit():
            return int(value)
        else:
            return value

config = AutoCastConfigParser()
config.read(INI_PATH, "utf-8")