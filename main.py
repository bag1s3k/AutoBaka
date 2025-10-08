import logging
import argparse
import time

from internal.core import Absence
from internal.core.page_model import MarksPage, Login, Timetable
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from internal.filesystem.paths_constants import PROJECT_ROOT
from internal.filesystem.ini_loader import config
from internal.utils.cloud_backup.backup import run_buckup

start_time = time.time() # STOPWATCH start

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# -------------------------------- BEFORE TO ENTER THE WEBSITE ---------------------------------- #
if not PROJECT_ROOT.exists():
    logger.error("Project root folder doesn't exist")


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

    # ----- MARKS ------ #
    marks_page = MarksPage(driver=driver, url=config.get_auto_cast("URLS", "marks_url"))
    marks_page.get()
    marks_page.get_marks()
    marks_page.process_marks()

    print(".", end="", flush=True)

    # ----- TIMETABLE ------ #
    timetable = Timetable(driver=driver, url=config.get_auto_cast("URLS", "timetable_url"))
    timetable.get()
    timetable.get_tt()

    print(".", end="", flush=True)

    # ----- ABSENCE ------ #
    absence = Absence(driver=driver, url=config.get_auto_cast("URLS", "absence_url"))
    absence.get()
    absence.get_absence()

    print(".", end="", flush=True) 

    # --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #
    if config.get_auto_cast("SETTINGS", "quit_driver"):  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")
    logger.info("Drive was successfully terminated")

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

# run_buckup() # it's only for me, it creates copy of the whole project except some files and folders