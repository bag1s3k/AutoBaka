import logging
import argparse
import time

from internal.core import Absence, Marks, Timetable, Login
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from internal.filesystem.paths_constants import PROJECT_ROOT
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
login = Login(driver=driver, url=config.get_auto_cast("URLS", "login_url"))
login.get()
login.login(username, password)

print(".", end="", flush=True)

# ----- MARKS ------ #
marks_page = Marks(driver=driver, url=config.get_auto_cast("URLS", "marks_url"))
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
if config.get_auto_cast("SETTINGS", "quit_driver") is not False:  # let window open or close it
    driver.quit()
    logger.info("driver was successfully quit")

print(". Successfully", flush=True) # CLI PRINT

print(f"{round(time.time() - start_time, 5)}s")