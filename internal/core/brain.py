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

    # === BEFORE TO ENTER THE WEBSITE === #
    # - setup driver for selenium
    # - create main parse for case user want to use CLI to login instead .env
    driver = setup_driver()

    # Load login details and create main_parser
    main_parser = argparse.ArgumentParser(
        prog=__name__,
        description="parses cmd-line args to extract user credentials (username and password)",
    )

    username, password = load_credentials(main_parser)

    print(".", end="", flush=True) # progress print

    # === ON WEBSITE === #
    # --- login --- #
    login = Login(driver=driver)
    if not login.get(config.get_auto_cast("URLS", "login_url")):
        failure.add(Login)
        driver.quit()
        return failure
    login.scrape(username, password)

    print(".", end="", flush=True)

    # --- marks --- #
    marks_page = Marks(driver=driver)
    if not marks_page.get(config.get_auto_cast("URLS", "marks_url")):
        failure.add(Marks)
    marks_page.scrape()
    export_json(marks_page.subjects, PATHS.raw_marks)
    marks_page.process_marks()
    export_json(marks_page.subjects, PATHS.processed_marks)
    export_results(marks_page.subjects, config.get_auto_cast("PATHS", "result_path_marks"))

    print(".", end="", flush=True)

    # --- timetable --- #
    timetable = Timetable(driver=driver)
    if not timetable.get(config.get_auto_cast("URLS", "timetable_url")):
        failure.add(Timetable)
    timetable.scrape()
    export_json(timetable.timetable, PATHS.two_weeks_timetable)

    print(".", end="", flush=True)

    # --- absence --- #
    absence = Absence(driver=driver)
    if not absence.get(config.get_auto_cast("URLS", "absence_url")):
        failure.add(Absence)
    absence.scrape()
    absence.calc_lectures(timetable.timetable, timetable.even_timetable, timetable.odd_timetable)
    export_json(absence.absence, PATHS.raw_absence)
    absence.calc_absence(timetable.timetable)
    export_json(absence.absence, PATHS.calculated_absence)
    with open(config.get_auto_cast("PATHS", "result_path_absence"), "w") as f:
        for subject in absence.absence:
            for k,v in subject.items():
                f.write(f"{k}: {v}\n-----\n")

    print(".", end="", flush=True)

    # === TERMINATE WEBDRIVER === #
    if config.get_auto_cast("SETTINGS", "quit_driver") is not False:  # let window open or close it
        driver.quit()
        logger.info("driver was successfully quit")

    print(".", flush=True) # CLI PRINT

    return failure