import logging
import sys

from internal.core.marks_processor import get_marks, process_marks
from internal.core.navigation import login
from internal.core.selenium_setup import setup_driver
from internal.filesystem.config_manager import get_config, setup_logging
from internal.filesystem.env_loader import load_credentials
from internal.utils.export import export_results

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def main():
    """
    Main script func, Launch app
    """
    logger.info("Launching main func of baka an app")

    driver = None

    try:
        # Initiation webdriver
        logger.info("Initiation webdriver")
        driver = setup_driver()
        logger.info("Initiation was successful")

        # Load login details
        logger.info("Loading login details")
        username, password = load_credentials()
        if not username or not password:
            logger.error("Missing loging details")
            return False
        logger.info(f"Loading was successful for user: {username}")

        # Login to baka
        logger.info("Logging to baka")
        login_success = login(driver, username, password)

        if not login_success:
            logger.error("Logging failed")
            return False

        logger.info("Logging was successful")

        # Get marks
        logger.info("Getting raw marks")
        raw_marks = get_marks(driver)

        if not raw_marks:
            logger.error("There is not any marks in the list")
            logger.error("Website might be changed")
            return False

        logger.info("Getting raw marks was successful")

        # Processing marks
        logger.info("Calculating averages")
        processed_marks = process_marks(raw_marks)

        if not processed_marks:
            logger.error("Calculating marks failed")
            return False

        logger.info("Calculating was successful")

        # Export results
        logger.info("Exporting results")
        export_success = export_results(processed_marks, get_config("PATHS", "result_path"))

        if not export_success:
            logger.error("Exporting failed")
            return False

        logger.info("Exporting was successful")

        # Finishing
        logger.info("Terminate webdriver")
        driver.quit()
        logger.info("Drive was successfully terminated")

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
    success = main()

    if success:
        logger.info("Program was completed successfully")
        print(0)
        sys.exit(0)
    else:
        logger.error("Program was terminated with an error")
        print(1)
        sys.exit(1)