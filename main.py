import logging
import sys
import argparse

from internal.core.marks_processor import get_marks, process_marks
from internal.core.navigation import login
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_loader import load_credentials
from internal.filesystem.export import export_results
from internal.filesystem.paths_constants import find_project_root
from internal.filesystem.ini_loader import config

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def main() -> bool:
    """
    Main base function

    Returns:
        Bool: True if successful, False otherwise
    """

    logger.info("Launching main func of baka an app")

    print(".", end="", flush=True) # CLI PRINT

    # Find root folder
    if not find_project_root() or not find_project_root().exists():
        logger.error("Root folder not found")
        return False

    if not config.read:
        logger.error("Config loading failed")
        return False

    driver = None

    # Start of app
    try:
        # Initiation webdriver
        logger.info("Initiation webdriver")
        driver = setup_driver()
        logger.info("Initiation was successful")

        print(".", end="", flush=True) # CLI PRINT

        # Load login details and create main_parser
        logger.info("Loading login details")
        main_parser = argparse.ArgumentParser(
            prog=__name__,
            description="main parser for main file",
        )

        username, password = load_credentials(main_parser)

        if not username or not password:
            logger.error("Missing loging details")
            return False
        logger.info(f"Loading was successful for user: {username}")

        print(".", end="", flush=True) # CLI PRINT

        # Login to baka
        logger.info("Logging to baka")
        login_success = login(driver, username, password)

        if not login_success:
            logger.error("Logging failed")
            return False

        logger.info("Logging was successful")

        print(".", end="", flush=True) # CLI PRINT

        # Get marks
        logger.info("Getting raw marks")
        raw_marks = get_marks(driver)

        if not raw_marks:
            logger.error("There is not any marks in the list")
            logger.error("Website might be changed")
            return False

        logger.info("Getting raw marks was successful")

        print(".", end="", flush=True) # CLI PRINT

        # Processing marks
        logger.info("Calculating averages")
        processed_marks = process_marks(raw_marks)

        if not processed_marks:
            logger.error("Calculating marks failed")
            return False

        logger.info("Calculating was successful")

        print(".", end="", flush=True) # CLI PRINT

        # Export results
        logger.info("Exporting results")
        if not export_results(processed_marks, config.get_config("PATHS", "result_path")):
            logger.error("Exporting failed")
            return False

        logger.info("Exporting was successful")

        print(".", end="", flush=True) # CLI PRINT

        # Finishing
        logger.info("Terminate webdriver")
        if config.get_config("SETTINGS", "quit_driver"): # let window open or close it
            driver.quit()
            logger.info("driver was successfully quit")
        logger.info("Drive was successfully terminated")

        print(".", end="", flush=True) # CLI PRINT

        return True

    except KeyboardInterrupt:
        logger.warning("Program was terminate by pressing ctrl+c")
        return False

    except Exception as e:
        logger.exception(f"Unexpectedly error... {str(e)}")
        logger.error("Program is gonna be terminate because of error")
        return False

    finally:
        # End Driver if the program crash
        if driver:
            try:
                logger.info("Terminate webdriver")
                driver.quit()
                logger.info("Webdriver was successfully terminated")
            except Exception as e:
                logger.error(f"Error during terminating program: {str(e)}")


def run() -> bool:
    """
    Helper run func

    Args:
        app (str):
            - "cli" for addition print in cmd
            - "gui" for gui
    """
    success = main()

    if success:
        print(" Successfully")

        logger.info("Program was completed successfully")
    else:
        print(" Error, results could be incomplete or wrong")

        logger.error("Program was terminated with an error")

if __name__ == "__main__":
    if run():
        sys.exit(0)
    else:
        sys.exit(1)