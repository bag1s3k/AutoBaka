import logging
import argparse
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from internal.core.page_model import MarksPage, Login, Timetable
from internal.core.web_processor import get_marks, process_marks, get_timetable, process_timetable, \
    get_permanent_timetable
from internal.core.web_navigation import go_to_url
# from internal.core.web_navigation import login, go_to_url
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

# -------------------------------- BEFORE TO ENTER THE WEBSITE ---------------------------------- #
# Does the PROJECT_ROOT path exist?
log_variable(PROJECT_ROOT.exists(),
                     level="critical",
                     error_msg="project root folder doesn't exist",
                     success_msg="Project root folder exists")


driver = None
try:
    driver = setup_driver()

    # Load login details and create main_parser
    main_parser = argparse.ArgumentParser(
        prog=__name__,
        description="parses cmd-line args to extract user credentials (username and password)",
    )
    username, password = load_credentials(main_parser)

    print(".", end="", flush=True) # progress print

    # ------------------------------------- ON WEBSITE -------------------------------------- #
    login = Login(driver=driver, url=config.get_auto_cast("URLS", "login_url"))
    login.get()
    login.login(username, password)

    print(".", end="", flush=True)

    # Marks page
    marks_page = MarksPage(driver=driver, url=config.get_auto_cast("URLS", "marks_url"))
    marks_page.get()
    marks_page.get_marks()

    print(".", end="", flush=True) 

    # TIMETABLE PAGE
    timetable = Timetable(driver=driver, url=config.get_auto_cast("URLS", "timetable_url"))
    timetable.get()
    timetable.get_timetable()

    print(".", end="", flush=True) 

    # --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #
    if config.get_auto_cast("SETTINGS", "quit_driver"):  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")
    logger.info("Drive was successfully terminated")

    # ------------------------------------ PROCESSING MARKS ------------------------------------ #
    processed_marks = process_marks(marks_page.SUBJECTS)

    print(".", end="", flush=True) # CLI PRINT

    # ------------------------------------ EXPORTING RESULTS ------------------------------------ #
    export_results(processed_marks, config.get_auto_cast("PATHS", "result_path"))

    print(". Successfully", flush=True) # CLI PRINT

except KeyboardInterrupt:logger.warning("Program was terminate by pressing ctrl+c")

except Exception as e: logger.exception(f"Unexpectedly error... {str(e)}")

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