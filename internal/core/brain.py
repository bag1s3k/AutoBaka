import logging
import argparse
from typing import Tuple

from internal.core import Absence, Marks, Timetable, Login
from internal.filesystem.export import export_json, export_results
from internal.utils.decorators import validate_output, timer
from internal.utils.selenium_setup import setup_driver
from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_utils import load_credentials
from paths_constants import PATHS
from internal.filesystem.ini_loader import config

@validate_output(
    error_msg="Main function execution failed",
    level="critical",
    allow_empty=True
)
@timer
def main_process() -> set | Tuple[set, bool]:
    failure = set() # List of failed scrapers

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
    if not login.get(config.get_auto_cast("URLS", "login_url")):
        failure.add(Login)
        driver.quit()
        logger.info("driver was successfully quit")
        return failure
    login.scrape(username, password)

    print(".", end="", flush=True)

    # ----- MARKS ------ #
    marks_page = Marks(driver=driver)
    if not marks_page.get(config.get_auto_cast("URLS", "marks_url")):
        failure.add(Marks)
    marks_page.scrape()
    export_json(marks_page.subjects, PATHS.raw_marks)
    marks_page.process_marks()
    export_json(marks_page.subjects, PATHS.processed_marks)
    export_results(marks_page.subjects, config.get_auto_cast("PATHS", "result_path"))

    print(".", end="", flush=True)

    # ----- TIMETABLE ------ #
    timetable = Timetable(driver=driver)
    if not timetable.get(config.get_auto_cast("URLS", "timetable_url")):
        failure.add(Timetable)
    timetable.scrape()
    export_json(timetable.timetable, PATHS.two_weeks_timetable)

    print(".", end="", flush=True)

    # ----- ABSENCE ------ #
    absence = Absence(driver=driver)
    if not absence.get(config.get_auto_cast("URLS", "absence_url")):
        failure.add(Absence)
    absence.scrape()
    absence.calc_lectures(timetable.timetable, timetable.even_timetable, timetable.odd_timetable)
    export_json(absence.absence, PATHS.raw_absence)
    absence.calc_absence(timetable.timetable)
    export_json(absence.absence, PATHS.calculated_absence)

    print(".", end="", flush=True)

    # --------------------------------------- TERMINATE WEBDRIVER ----------------------------- #
    if config.get_auto_cast("SETTINGS", "quit_driver") is not False:  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")

    print(".", flush=True) # CLI PRINT

    return failure