import logging
import argparse
import time

from internal.core.marks_processor import get_marks, process_marks
from internal.core.web_navigation import login
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from internal.filesystem.export import export_results
from internal.filesystem.paths_constants import PROJECT_ROOT
from internal.filesystem.ini_loader import config
from internal.utils.decorators import log_message
from internal.utils.var_validator import log_variable
import internal.utils.cloud_backup.backup # TODO do it in the background

start_time = time.time() # STOPWATCH start

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

@log_message("Main function (brain) failed", "Main function (brain) successfully completed", "critical")
def main() -> bool:

    # Find root folder
    if not log_variable(PROJECT_ROOT.exists(), "error", "project root doesn't exist", "Project root folder exist"): return False

    # Read config
    if not log_variable(config.read, "config.read", "critical"): return False

    driver = None

    # Start of an app
    try:
        # Initiation webdriver
        driver = setup_driver()

        # Load login details and create main_parser
        logger.info("Loading login details")
        main_parser = argparse.ArgumentParser(
            prog=__name__,
            description="main parser for main file",
        )

        username, password = load_credentials(main_parser)

        if not log_variable(username or password, "critical"): return False

        print(".", end="", flush=True) # CLI PRINT

        # Login to baka

        if not log_variable(login(driver, username, password), "critical", "login failed", "Login successful"):
            return False

        print(".", end="", flush=True) # CLI PRINT

        # Get marks
        raw_marks = get_marks(driver)
        if not log_variable(raw_marks, "critical", "get marks failed", "get marks successful"):
            return False

        print(".", end="", flush=True) # CLI PRINT

        # Processing marks
        logger.info("Calculating averages")
        processed_marks = process_marks(raw_marks)

        if not log_variable(processed_marks, "warning", "No marks to process"): return False

        print(".", end="", flush=True) # CLI PRINT

        # Export results
        logger.info("Exporting results")
        if not log_variable(export_results(processed_marks, config.get_config("PATHS", "result_path")), "error", "Nothing wrote"):
            return False

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

    # finally:
    #     # End Driver if the program crash
    #     if driver:
    #         try:
    #             logger.info("Terminate webdriver")
    #             if config.get_config("SETTINGS", "quit_driver"):  # let window open or close it
    #                 driver.quit()
    #                 logger.info("driver was successfully quit")
    #             logger.info("Drive was successfully terminated")
    #         except Exception as e:
    #             logger.error(f"Error during terminating program: {str(e)}")


if __name__ == "__main__":
    main()
    print(f"{round(time.time() - start_time, 5)}s")