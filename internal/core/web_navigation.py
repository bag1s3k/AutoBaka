import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from internal.filesystem.ini_loader import config
from internal.utils.decorators import validate_output

logger = logging.getLogger(__name__)


@validate_output(error_msg="Login func failed", success_msg="Login successful", level="critical")
def login(driver, username: str, password: str) -> bool | None:
    """
    Login user to baka page, send login details to page
    :param driver: instance of the driver
    :param username: username (string)
    :param password: password (string)
    :return bool: Successful?
    """

    try:
        driver.get(config.get_auto_cast("URLS", "login_url")); logger.debug("Website loaded")

        # Find required elements on website (username and password field, login button)
        username_field = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
            ec.presence_of_element_located((By.NAME, "username"))
        )
        logger.debug("Field for username found")

        password_field = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
            ec.presence_of_element_located((By.NAME, "password"))
        )
        logger.debug("Field for password found")

        login_button = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
            ec.presence_of_element_located((By.NAME, "login"))
        )
        logger.debug("Login button found")

        username_field.clear()
        username_field.send_keys(username); logger.debug(f"Username filled: {username}")
        password_field.clear()
        password_field.send_keys(password); logger.debug("Password filled: <MASKED>")
        login_button.click(); logger.debug("Click the button")

        return True

    except Exception as e:
        logger.exception(f"Login failed: {e}")


@validate_output(error_msg="Moving to new url failed", success_msg="Moving to new url successful", level="critical")
def go_to_url(driver, url) -> bool | None:
    """Navigation to the targe url
    :param driver: instance of webdriver
    :param url: target url
    :return bool: True on success False otherwise
    """

    try:
        logger.debug("Go to the target page")

        driver.get(url)

        logger.debug("Wait until page will load")

        logger.info("Target page was successfully load")
        return True

    except Exception as e:
        logger.exception(f"Error while moving to the target page: {e}")
        logger.debug(f"Current url: {driver.current_url}")
        logger.debug(f"Current title: {driver.title}")