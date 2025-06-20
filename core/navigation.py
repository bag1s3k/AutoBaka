import logging
import time

from selenium.webdriver.common.by import By
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
        driver.get(get_config("URLS", "login_url"))
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "login").click()
        time.sleep(2)
        driver.get(get_config("URLS", "marks_url"))
        time.sleep(1)

        return True
    except Exception as e:
        pass