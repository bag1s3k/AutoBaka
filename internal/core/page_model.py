import logging
from typing import Tuple
from abc import ABC

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
    def __init__(self, driver, url, timeout=config.get_auto_cast("SETTINGS", "timeout")):
        self.driver = driver
        self.timeout = timeout
        self.url = url

    @validate_output(
        error_msg=f"Moving to the target page failed url",
        success_msg=f"Moving to the target page successful url:",
        level="critical"
    )
    def get(self):
        """Move to target page"""
        try:
            self.driver.get(self.url)
            return True
        except Exception as e:
            logger.exception(e)
            self.driver.quit()
            return False

    @validate_output(
        error_msg="Item on website not found",
        success_msg="Item on website found",
        level="warning"
    )
    def _find_item(self, target: Tuple[str, str], parent=None) -> WebElement | None:
        """ Find specific element on website
            :param target: tuple selenium expression e.g (By.XPATH, "//div")
            :param parent: Selenium WebElement; default self.driver If None
            :return item: If true return matching element otherwise return None
        """
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_element_located(target)
            )
            return item
        except Exception as e:
            logger.warning(e)
            return None

    @validate_output(
        error_msg="Items not found",
        success_msg="Items found",
        level="warning"
    )
    def _find_items(self, target: Tuple[str, str], parent=None) -> list[WebElement] | None:
        """ Find specific elements on website
            :param target: tuple selenium expression e.g (By.XPATH, "//div")
            :param parent: Selenium WebElement; default self.driver If None
            :return item: If true return matching elements otherwise return None"""
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_all_elements_located(target)
            )
            return item
        except Exception as e:
            logger.warning(e)
            return None