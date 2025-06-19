import time

from selenium.webdriver.common.by import By
from config.logging_conf import setup_logging
from config.config_manager import get_config

setup_logging()

def login(driver, username, password):
    driver.get(get_config("URLS", "login_url"))
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(2)
    driver.get(get_config("URLS", "marks_url"))
    time.sleep(1)

    return True