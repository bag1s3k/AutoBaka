import json
import logging

from internal.core.brain import main_process
from internal.core import Absence, Marks, Timetable, Login
from internal.filesystem.paths_constants import MARKS_OUTPUT, TIMETABLE_OUTPUT, RAW_ABSENCE_OUTPUT
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

if not (failure := main_process()):
   logger.info("Main process ended with no error")


def get_local_json_data(path: str, encode="utf-8"):
    """Get local data when interaction on website fail
    :param path: source path
    :param encode: encoding
    :return json as a python readable format"""
    with open(path, "r", encoding=encode) as f:
        f_data = json.load(f)
        return f_data


for scraper in failure:
    # ----- LOGIN ----- #
    if scraper is Login:
        logger.error("Loading last local data")
        marks = get_local_json_data(MARKS_OUTPUT)
        timetable = get_local_json_data(TIMETABLE_OUTPUT)
        absence = get_local_json_data(RAW_ABSENCE_OUTPUT)
    # ----- MARKS ----- #
    if scraper is Marks:
        logger.error("Loading last local marks data")
        marks = get_local_json_data(MARKS_OUTPUT)

    # ----- ABSENCE ----- #
    if scraper is Absence:
        logger.error("Loading last local absence data")
        absence = get_local_json_data(RAW_ABSENCE_OUTPUT)

    # ----- TIMETABLE ----- #
    if scraper is Timetable:
        logger.error("Loading last local timetable data")
        timetable = get_local_json_data(TIMETABLE_OUTPUT)