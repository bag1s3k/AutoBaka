import logging

from selenium.webdriver.common.by import By

from ..page_model import BasePage
from internal.utils.decorators import validate_output
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class Login(BasePage):
    """
    Inherits from BasePage
    Use for login
    """

    @validate_output(
        error_msg="Login failed",
        success_msg="Login successful",
        level="critical"
    )
    def login(self, username, password) -> bool:
        """
        Specific login logic
        :param username: username (string)
        :param password: password (string)
        :return: True if successful otherwise False
        """
        # Find required elements on website (username and password field, login button)
        username_field = self._find_item(target=(By.NAME, "username"))
        password_field = self._find_item(target=(By.NAME, "password"))
        login_button = self._find_item(target=(By.NAME, "login"))

        try:
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()

            return True
        except Exception as e:
            logger.exception(e)
            return False