# v1.3.0

import logging
import sys
import argparse
import time

from internal.core.marks_processor import get_marks, process_marks
from internal.core.navigation import login
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_loader import load_credentials
from internal.filesystem.export import export_results
from internal.filesystem.paths_constants import find_project_root
from internal.filesystem.ini_loader import config
from internal.utils.decorators import message
from internal.utils.var_validator import var_message

# STOPWATCH
t1 = time.time()

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

@message("Main function (brain) failed", "Main function (brain) successfully completed", "critical")
def main() -> bool:
    """
    Main base function

    Returns:
        Bool: True if successful, False otherwise
    """

    print(".", end="", flush=True) # CLI PRINT

    # Find root folder
    if not var_message(find_project_root().exists(), "find_project_root().exist()", "error", "project root doesn't exist", "Project root folder exist"):
        return False

    # Read config
    if not var_message(config.read, "config.read", "critical"):
        return False

    driver = None

    # Start of app # TODO START
    try:
        # Initiation webdriver
        driver = setup_driver()

        print(".", end="", flush=True) # CLI PRINT

        # Load login details and create main_parser
        logger.info("Loading login details")
        main_parser = argparse.ArgumentParser(
            prog=__name__,
            description="main parser for main file",
        )

        username, password = load_credentials(main_parser)

        if not var_message(username or password, "username | password", "critical"):
            return False

        print(".", end="", flush=True) # CLI PRINT

        # Login to baka

        if not var_message(login(driver, username, password), "login(driver, username, password)", "critical", "login failed", "Login successful"):
            return False

        print(".", end="", flush=True) # CLI PRINT

        # Get marks
        raw_marks = get_marks(driver)
        if not var_message(raw_marks, "raw_marks", "critical", "get marks failed", "get marks successful"):
            return False

        print(".", end="", flush=True) # CLI PRINT

        # Processing marks
        logger.info("Calculating averages")
        processed_marks = process_marks(raw_marks)

        if not var_message(processed_marks, "processed_marks", "warning", "no marks to process"):
            return False

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

        print(". Successfully", flush=True) # CLI PRINT

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

if __name__ == "__main__":
    main()
    print(f"{round(time.time() - t1, 5)}s")