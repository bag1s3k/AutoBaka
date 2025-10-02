import logging
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from unidecode import unidecode

from internal.filesystem.export import export_json
from internal.filesystem.ini_loader import config
from internal.filesystem.paths_constants import JSON_OUTPUT_PATH, JSON_RAW_OUTPUT_PATH
from internal.utils.decorators import log_message
from internal.utils.var_validator import log_variable

logger = logging.getLogger(__name__)


@log_message(error_message="Extraction marks from baka page failed",
             right_message="Extraction marks from baka page successful",
             level="warning")
def get_marks(driver, xpath: str) -> dict:
    """
    Extraction marks from baka page
    :param driver: instance of the browser
    :param xpath: xpath of marks
    :return subjects: dictionary {subject: average}
    """

    try:
        logger.info("Looking for an element on page with marks")

        marks_line = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
            ec.presence_of_all_elements_located((By.XPATH, xpath))
        )

        # Load whole marks (date, mark, value...) it's line of these data
        if not log_variable(marks_line,
                            level="warning",
                            error_message=f"Marks not found url: {driver.current_url} title: {driver.title}",
                            right_message=f"Marks found url {driver.current_url} title: {driver.title}"):
            return {}

        # Extract marks to a dict
        logger.info("Extracting marks data to variable")

        subjects = {}
        for single_line in marks_line:
            subject = WebDriverWait(single_line, config.get_auto_cast("SETTINGS", "timeout")).until(
                ec.presence_of_all_elements_located((By.TAG_NAME, "td"))
            )

            if not log_variable(subject,
                                level="warning",
                                error_message="No subject",
                                right_message="Subject found"):
                return {}

            mark = subject[1].text
            topic = unidecode(subject[2].text)
            weight = subject[5].text
            date = subject[6].text
            subject_name = unidecode(subject[0].text)

            logger.info(f"Extracting: {mark} {topic} {weight} {date} {subject_name}")

            subjects.setdefault(subject_name, []).append({
                "mark": mark,
                "topic": topic,
                "weight": weight,
                "date": date
            })

        # Export marks to json file
        export_json(subjects, JSON_RAW_OUTPUT_PATH)

        return subjects

    except Exception as e:
        logger.exception(f"Issue during getting marks: {str(e)}")
        return {}


@log_message(error_message="Processing marks failed", right_message="Processing marks successful", level="critical")
def process_marks(subjects: dict) -> dict:
    """
    Processing marks and calculate averages
    :param subjects: dict of marks
    :return subjects: sorted dict of processed marks
    """

    if not subjects: return {}

    logger.info(f"Processing marks")

    # (1- -> 1.5) or N don't add to the list and Calculate average
    text_to_num = [4.5, 3.5, 2.5, 1.5]
    for subject, list_subject in subjects.items():
        logger.info(f"Processing subject: {subject}")
        try:
            marks = []
            for dict_mark in list_subject:
                if "-" in dict_mark["mark"]:
                    dict_mark["mark"] = text_to_num[-int(dict_mark["mark"][0])] # take 1. char of '2-' => 2 and 2 * (-1) => -2 is index of a list (text_to_num)
                elif dict_mark["mark"].isdigit():
                    dict_mark["mark"] = int(dict_mark["mark"])
                else:
                    continue

                marks.append([dict_mark["mark"], dict_mark["weight"]])

            # Calculate averages
            logger.info("Calculating average")

            mark_times_weight = 0
            weight_sum = 0

            for mark in marks:
                mark_times_weight += float(mark[0]) * float(mark[1])
                weight_sum += float(mark[1])

            average = 0
            if weight_sum != 0:
                average = round(mark_times_weight / weight_sum, 2)
            else:
                logger.warning(f"{subject} has no weight")

            subjects[subject].append({"avg": average})

            # Export marks to json file
            export_json(subjects, JSON_OUTPUT_PATH)

        except Exception as e:
            logger.exception(f"Something happened during processing marks: {e}")
            return {}

    return dict(sorted(subjects.items()))


@log_message(error_message="Extracting timetable failed",
             right_message="Extracting timetable successful",
             level="critical")
def get_timetable(driver, xpath: str) -> dict:
    """
    Extract timetable from website
    :param driver: an instance of chromedriver
    :param xpath: xpath for each day
    :return timetable: timetable (dict)
    """

    timetable = {}
    try:
        days = WebDriverWait(driver, config.get_auto_cast("SETTINGS", "timeout")).until(
            ec.presence_of_all_elements_located(("xpath", xpath))
        )
        print(days)

        if n_days := len(days) != 5:
            logger.debug(f"Wrong amount of days: {n_days} there must be 5")

        for day in days:
            date = WebDriverWait(day, config.get_auto_cast("SETTINGS", "timeout")).until(
                ec.presence_of_element_located(("xpath", ".//div/div/div/div/span")))
            date = date.text

            lectures = WebDriverWait(day, config.get_auto_cast("SETTINGS", "timeout")).until(
                ec.presence_of_all_elements_located(("xpath", ".//div/div/span/div/div[@class='empty'] |"
                                                  ".//div/div/span/div/div/div[@class='top clearfix'] |"
                                                  ".//div/div/span/div/div/div/div[2]")))

            timetable[date] = []
            for lecture in lectures:
                timetable[date].append(lecture.text)

            if (n_timetable := len(timetable[date])) != 10:
                logger.debug(f"Wrong amount of lectures: {n_timetable} there must be 10")

    except Exception as e:
        logger.exception(f"Something unexcepted happened: {e}")
        return {}

    return timetable


def get_permanent_timetable(driver):
    time.sleep(2)
    xpath_lessons = "//div/div/div/span/div/div[@class='empty'] | //div/div/div/span/div/div/div/div[2]"
    days_timetable = "//div[@class='day-row double']"

    days = driver.find_elements("xpath", days_timetable)

    for day in days:
        day_t = day.find_elements("xpath", xpath_lessons)

        for d in day_t:
            print(d.text)

def process_timetable(timetable):
    for k, v in timetable.items():
        print(k, v)