import logging
import argparse
import time

from internal.core import Absence, Marks, Timetable, Login
from internal.filesystem.export import export_json, export_results
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from internal.filesystem.paths_constants import PROJECT_ROOT, RAW_MARKS_OUTPUT, MARKS_OUTPUT, TIMETABLE_OUTPUT, \
    RAW_ABSENCE_OUTPUT
from internal.filesystem.ini_loader import config

start_time = time.time() # STOPWATCH start

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

# -------------------------------- BEFORE TO ENTER THE WEBSITE ---------------------------------- #
if not PROJECT_ROOT.exists():
    logger.error("Project root folder doesn't exist")

driver = setup_driver()

# Load login details and create main_parser
main_parser = argparse.ArgumentParser(
    prog=__name__,
    description="parses cmd-line args to extract user credentials (username and password)",
)

username, password = load_credentials(main_parser)

print(".", end="", flush=True) # progress print

# ------------------------------------- ON WEBSITE -------------------------------------- #
login = Login(driver=driver)
login.get(config.get_auto_cast("URLS", "login_url"))
login.scrape(username, password)

print(".", end="", flush=True)

# ----- MARKS ------ #
marks_page = Marks(driver=driver)
marks_page.get(config.get_auto_cast("URLS", "marks_url"))
marks_page.scrape()
export_json(marks_page.subjects, RAW_MARKS_OUTPUT)
marks_page.process_marks()
export_json(marks_page.subjects, MARKS_OUTPUT)
export_results(marks_page.subjects, config.get_auto_cast("PATHS", "result_path"))

print(".", end="", flush=True)

# ----- TIMETABLE ------ #
timetable = Timetable(driver=driver)
timetable.get(config.get_auto_cast("URLS", "timetable_url"))
timetable.scrape()
export_json(timetable.timetable, TIMETABLE_OUTPUT)

print(".", end="", flush=True)

# ----- ABSENCE ------ #
absence = Absence(driver=driver)
absence.get(config.get_auto_cast("URLS", "absence_url"))
absence.scrape()
export_json(absence.absence, RAW_ABSENCE_OUTPUT)

print(".", end="", flush=True)

# --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #
if config.get_auto_cast("SETTINGS", "quit_driver") is not False:  # let window open or close it
    driver.quit()
    logger.info("driver was successfully quit")

print(". Successfully", flush=True) # CLI PRINT

print(f"{round(time.time() - start_time, 5)}s")