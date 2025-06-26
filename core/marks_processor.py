# conflict maker
import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode
from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def get_marks(driver) -> dict:
    """
    Extraction marks from baka page
    Args:
        driver: instance of the browser
    Returns:
        dict: dictionary {subject: average}
    """

    try:
        logger.info("Looking for an element on page with marks")
        marks_line = driver.find_elements("xpath",
                                          "//tbody//tr[.//td and contains(@class, 'dx-row') and contains(@class, 'dx-data-row') and contains(@class, 'dx-row-lines')]")

        # Load whole marks (date, mark, value...) it's line
        if not marks_line:
            logger.error("No mark found")
            logger.debug(f"Current url: {driver.current_url}")
            logger.debug(f"Current title: {driver.title}")

            return {}

        logger.info("Marks found")
        subjects = {}

        # Extract marks to a dict
        logger.info("It's gonna extract marks to a list")
        for single_line in marks_line:
            subject = single_line.find_elements(By.TAG_NAME, "td")

            if not subject:
                logger.error("Error during extraction marks")

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

            logger.info(f"Extracted: {mark} {topic} {weight} {date} {subject_name}")

        return subjects

    except Exception as e:
        logger.exception(f"Issue during getting marks: {str(e)}")
        return {}

def process_marks(subjects) -> dict:
    """
    Processing marks (1- -> 1.5 or N -> don't add)
    Calculate averages
    Args:
        subjects: dict of marks
    Returns:
        dict: sorted dict of processed marks
    """

    if not subjects:
        logger.warning("No marks to process")
        return {}

    logger.info(f"Processing marks")

    # 1- -> 1.5 or N -> don't add and Calculate average
    for subject, list_subject in subjects.items():
        logger.info(f"Processing subject: {subject}")
        try:
            marks = []
            for dict_mark in list_subject:
                if "-" in dict_mark["mark"]:
                    text_to_num = [4.5, 3.5, 2.5, 1.5]
                    dict_mark["mark"] = dict_mark["mark"][::-1]
                    dict_mark["mark"] = text_to_num[int(dict_mark["mark"])]
                elif not dict_mark["mark"].isdigit():
                    continue

                marks.append([dict_mark["mark"], dict_mark["weight"]])

            logger.info(f"Processing completed successfully")
            logger.info("Calculating average")
            # Calculate averages
            mark_times_weight = 0
            weight_sum = 0

            for mark in marks:
                mark_times_weight += float(mark[0]) * float(mark[1])
                weight_sum += float(mark[1])

            average = str(mark_times_weight / weight_sum)[:4]
            subjects[subject].append({"avg": average})

            logger.info("Calculating completed successfully")

        except Exception as e:
            logger.exception(f"Something happened during processing marks")
            return {}

    logger.info("Subject is gonna be sorted and returned")
    return dict(sorted(subjects.items()))