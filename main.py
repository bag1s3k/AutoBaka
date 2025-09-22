import logging
import argparse
import sys
import time

from internal.core.marks_processor import get_marks, process_marks
from internal.core.web_navigation import login, go_to_url
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from internal.filesystem.export import export_results
from internal.filesystem.paths_constants import PROJECT_ROOT
from internal.filesystem.ini_loader import config
from internal.utils.var_validator import log_variable

from internal.utils.cloud_backup.backup import run_buckup

start_time = time.time() # STOPWATCH start

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# -------------------------------- PREPARE TO ENTER THE WEBSITE ---------------------------------- #

# Does the PROJECT_ROOT path exist
if not log_variable(PROJECT_ROOT.exists(), "error", "project root doesn't exist", "Project root folder exist"): sys.exit(-1)

driver = None

try:

    driver = setup_driver() # Initiation webdriver

    # Load login details and create main_parser
    main_parser = argparse.ArgumentParser(
        prog=__name__,
        description="main parser for main file",
    )
    username, password = load_credentials(main_parser)
    if not username or not password: sys.exit(-1)

    print(".", end="", flush=True) # progress print

    if not login(driver, username, password): sys.exit(-1)
    if not go_to_url(driver, config.get_auto_cast("URLS", "marks_url")): sys.exit(-1)

    print(".", end="", flush=True) # progress print
    
    # ------------------------------------- ON THE WEBSITE -------------------------------------- #
    if not (raw_marks := get_marks(driver)): sys.exit(-1)

    print(".", end="", flush=True) # progress print

    # --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #

    if config.get_auto_cast("SETTINGS", "quit_driver"):  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")
    logger.info("Drive was successfully terminated")

    # ------------------------------------ PROCESSING MARKS ------------------------------------ #

    if not (processed_marks := process_marks(raw_marks)): sys.exit(-1)

    print(".", end="", flush=True) # CLI PRINT

    # ------------------------------------ EXPORTING RESULTS ------------------------------------ #

    if not export_results(processed_marks, config.get_auto_cast("PATHS", "result_path")): sys.exit(-1)

    print(". Successfully", flush=True) # CLI PRINT

except KeyboardInterrupt:
    logger.warning("Program was terminate by pressing ctrl+c")

except Exception as e:
    logger.exception(f"Unexpectedly error... {str(e)}")
    logger.error("Program is gonna be terminate because of error")

# finally:
#     # End Driver if the program crash
#     if driver:
#         try:
#             logger.info("Terminate webdriver")
#             if config.get_auto_cast_config("SETTINGS", "quit_driver"):  # let window open or close it
#                 driver.quit()
#                 logger.info("driver was successfully quit")
#             logger.info("Drive was successfully terminated")
#         except Exception as e:
#             logger.error(f"Error during terminating program: {str(e)}")


print(f"{round(time.time() - start_time, 5)}s")

run_buckup() # it's only for me, it creates copy of the whole project except some files and folders