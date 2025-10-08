import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from internal.filesystem.ini_loader import config
from internal.utils.decorators import validate_output

logger = logging.getLogger(__name__)


@validate_output(
    error_msg="Webdriver setup failed",
    success_msg="Webdriver setup successfully completed",
    level="error"
)
def setup_driver():
    """
    Setup chromedriver
    :return: an instance of driver
    """
    options = Options()

    # Set default configuration if there is no data in .ini for quit_driver (True default)
    logger.debug("Setup chrome options")
    if config.get_auto_cast("SETTINGS", "quit_driver"): # returns True or False
        options.add_experimental_option("detach", False)
        logger.debug("Detach False")
    else:
        options.add_experimental_option("detach", True)
        logger.debug("Detach True")

    # Set default configuration if there is no data in .ini for headless mode (True default)
    if config.get_auto_cast("SETTINGS", "headless_mode"): # returns True or False
        options.add_argument("--headless=new")
        logger.debug("Headless mode was activated")
    else:
        logger.debug("Headless mode off")

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)

    # Performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--window-size=1920,1080")

    # Suppress Chrome internal logs
    options.add_argument("--log-level=3")
    options.add_argument("--silent")

    try:
        # Installation and setup chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        return driver
    except Exception as e:
        logger.exception(f"Issue while installing or setting webdriver: {e}")