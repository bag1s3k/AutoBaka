import logging
import argparse
import sys
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from internal.core.web_processor import get_marks, process_marks, get_timetable, process_timetable
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

error_n = -1
def sysexit(var):
    """
    Checks variable and when the variable is falsy it stops the program and raises code num
    :param var: checking variable
    """
    global error_n
    if not var:
        sys.exit(error_n)
    else:
        error_n -= 1

# -------------------------------- PREPARE TO ENTER THE WEBSITE ---------------------------------- #
# Does the PROJECT_ROOT path exist
sysexit(log_variable(PROJECT_ROOT.exists(),
                     level="critical",
                     error_message="project root folder doesn't exist",
                     right_message="Project root folder exists"))

driver = None

try:
    driver = setup_driver() # Initiation webdriver

    # Load login details and create main_parser
    main_parser = argparse.ArgumentParser(
        prog=__name__,
        description="parses cmd-line args to extract user credentials (username and password)",
    )
    username, password = load_credentials(main_parser)

    sysexit(username or password)

    print(".", end="", flush=True) # progress print

    # ------------------------------------- ON THE WEBSITE -------------------------------------- #
    sysexit(login(driver, username, password))

    # Navigate to marks page
    marks_xpath = ("//tbody//tr[//td "
                   "and contains(@class, 'dx-row') "
                   "and contains(@class, 'dx-data-row') "
                   "and contains(@class, 'dx-row-lines')]")

    sysexit(go_to_url(driver, config.get_auto_cast("URLS", "marks_url")))

    print(".", end="", flush=True) 

    sysexit((raw_marks := get_marks(driver, marks_xpath)))

    print(".", end="", flush=True) 

    # Navigating on the timetable page
    # This week
    timetable_xpath = "//div[@class='day-row normal']"
    sysexit(go_to_url(driver, config.get_auto_cast("URLS", "timetable_url")))
    sysexit((thisweek_timetable := get_timetable(driver, timetable_xpath)))
    process_timetable(thisweek_timetable)

    print(".", end="", flush=True) 

    # Next week
    nextweek_timetable_btn = '//*[@id="cphmain_linkpristi"]'
    nextweek_button = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
        ec.presence_of_element_located(("xpath", nextweek_timetable_btn))
    )
    sysexit(nextweek_button)
    nextweek_button.click()
    sysexit((nextweek_timetable := get_timetable(driver, timetable_xpath)))
    process_timetable(nextweek_timetable)

    # permanent week
    permanentweek_timetable_btn = '//*[@id="cphmain_linkpevny"]'
    permanentweek_button = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
        ec.presence_of_element_located(("xpath", permanentweek_timetable_btn))
    )
    sysexit(permanentweek_button)
    permanentweek_button.click()

    print(".", end="", flush=True) 

    # --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #
    if config.get_auto_cast("SETTINGS", "quit_driver"):  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")
    logger.info("Drive was successfully terminated")

    # ------------------------------------ PROCESSING MARKS ------------------------------------ #
    sysexit((processed_marks := process_marks(raw_marks)))

    print(".", end="", flush=True) # CLI PRINT

    # ------------------------------------ EXPORTING RESULTS ------------------------------------ #
    sysexit(export_results(processed_marks, config.get_auto_cast("PATHS", "result_path")))

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