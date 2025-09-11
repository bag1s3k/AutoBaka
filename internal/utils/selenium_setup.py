import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from internal.filesystem.ini_loader import config
from internal.utils.decorators import log_message

logger = logging.getLogger(__name__)

@log_message("Webdriver setup failed", "Webdriver setup successfully completed", "error")
def setup_driver():
    """
    Setup chrome driver with optimization and settings
    Returns:
        webdriver.Chrome
    """
    try:
        options = Options()

        # Default configuration
        logger.debug("Setup chrome options")
        if config.get_config("SETTINGS", "quit_driver"):
            options.add_experimental_option("detach", False)
            logger.debug("Detach False")
        else:
            options.add_experimental_option("detach", True)
            logger.debug("Detach True")

        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)

        # Headless mode
        if config.get_config("SETTINGS", "headless_mode"): # Turn on or off headless mode from config.ini
            options.add_argument("--headless=new")
            logger.debug("Headless mode was activated")
        else:
            logger.debug("Headless mode off")

        # Performance
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--window-size=1920,1080")
        logger.debug("Performance optimization")

        # Suppress Chrome internal logs
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        logger.debug("Chrome logs suppressed")

        # Installation and setup chrome driver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        logger.info("Chrome was successfully started")
        return driver

    except Exception as e:
        logger.exception(f"Issue during installing or setup webdriver: {e}")
        raise e