import logging
from typing import Tuple
from abc import ABC, abstractmethod

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from internal.utils.decorators import validate_output
from internal.filesystem.ini_loader import config
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class BasePage(ABC):
    """ Abstract base class for using selenium (generally every interact with website)
        - every subclass is specific for 1 interaction (e.g. class Login)"""
    def __init__(self, driver, timeout=config.get_auto_cast("SETTINGS", "timeout")):
        self.driver = driver
        self.timeout = timeout

    @validate_output(
        error_msg=f"Moving to the target page failed url",
        success_msg=f"Moving to the target page successful url:",
        level="critical"
    )
    def get(self, url: str):
        """Move to target page"""
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            logger.critical(e)
            self.driver = None
            return False

    @validate_output(
        error_msg="Item on website not found",
        success_msg="Item on website found",
        level="warning"
    )
    def _find_item(self, target: Tuple[str, str], parent=None, mult=False) -> WebElement | list[WebElement] | None:
        """ Find specific element on website
            :param target: tuple selenium expression e.g (By.XPATH, "//div")
            :param parent: Selenium WebElement; default self.driver If None
            :return item: If true return matching element otherwise return None"""
        if parent is None:
            parent = self.driver

        if self.driver is None:
            return None

        try:
            if mult:
                item = WebDriverWait(parent, self.timeout).until(
                    ec.presence_of_all_elements_located(target)
                )
            else:
                item = WebDriverWait(parent, self.timeout).until(
                    ec.presence_of_element_located(target)
                )
            return item
        except Exception as e:
            logger.warning(e)
            return None

    @abstractmethod
    @validate_output()
    def scrape(self):
        """Specific scrape logic"""
        pass