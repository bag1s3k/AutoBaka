import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config.logging_conf import setup_logging
from config.config_manager import get_config

setup_logging()
logger = logging.getLogger(__name__)

def login(driver, username: str, password: str) -> bool:
    """
    Login user to app

    Args:
         driver: instance of the driver
         username: username (string)
         password: password (string)

    Return:
        bool: Was the login successful?
    """
    try:
        logger.info("Finding website")
        driver.get(get_config("URLS", "login_url"))
        logger.debug("Website loaded")

        # Wait until  username field load
        try:
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            logger.debug("Field for username found")

        except TimeoutException:
            logger.error("Field for username wasn't find")
            return False

        # Enter username detail
        logger.info("Entering username")
        username_field.clear()
        username_field.send_keys(username)
        logger.debug(f"Username filled: {username}")

        # Try to enter password
        try:
            password_field = driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            logger.debug("Password filled")

        except NoSuchElementException:
            logger.error("Field wasn't find")
            return False

        # Login button
        try:
            login_button = driver.find_element(By.NAME, "login")
            logger.debug("Login button found")

        except NoSuchElementException:
            logger.error("Login button not found")
            return False

        logger.info("Sending login form")
        login_button.click()

        logger.debug("Waiting after login")
        time.sleep(2)

    except Exception as e:
        logger.error(f"Issue during login: {e}")
        return False

    try:
        # Go to marks page
        logger.debug("Got to marks page")
        driver.get(get_config("URLS", "marks_url"))

        logger.debug("Wait until page will load")

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//tbody//tr[.//td and contains(@class, 'dx-row') and contains(@class, 'dx-data-row') and contains(@class, 'dx-row-lines')]"))
            )
            logger.info("Page with marks was successfully load")
            return True

        except TimeoutException:
            logger.error("Page with marks didn't load")
            logger.debug(f"Current url: {driver.current_url}")
            logger.debug(f"Current title: {driver.title}")
            return False

    except Exception as e:
        logger.error(f"Error while going to marks page: {e}")
        return False