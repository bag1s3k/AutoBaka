import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode
from internal.filesystem.json_export import export_json
from internal.filesystem.paths_constants import JSON_OUTPUT_PATH, JSON_RAW_OUTPUT_PATH
from internal.utils.decorators import message
from internal.utils.var_validator import var_message

logger = logging.getLogger(__name__)

@message("Get marks failed", "Get marks successful", "critical")
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
        if not var_message(marks_line, "marks_line", "warning", f"Marks not found url: {driver.current_url} title: {driver.title}", f"Marks found url {driver.current_url} title: {driver.title}"):
            return {}

        subjects = {}

        # Extract marks to a dict
        logger.info("It will extract marks to a list")
        for single_line in marks_line:
            subject = single_line.find_elements(By.TAG_NAME, "td")

            var_message(subject, "subject")

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

        # Export marks to json file
        export_json(subjects, JSON_RAW_OUTPUT_PATH)

        return subjects

    except Exception as e:
        logger.exception(f"Issue during getting marks: {str(e)}")
        return {}

@message("Processing marks failed", "Processing marks successful", "critical")
def process_marks(subjects) -> dict:
    """
    Processing marks and calculate averages

    Args:
        subjects: dict of marks

    Returns:
        dict: sorted dict of processed marks
    """

    if not var_message(subjects, "subjects", "warning", "No marks to process"):
        return {}

    logger.info(f"Processing marks")

    # 1- -> 1.5 or N don't add and Calculate average
    text_to_num = [4.5, 3.5, 2.5, 1.5]
    for subject, list_subject in subjects.items():
        logger.info(f"Processing subject: {subject}")
        try:
            marks = []
            for dict_mark in list_subject:
                if "-" in dict_mark["mark"]:
                    dict_mark["mark"] = text_to_num[-int(dict_mark["mark"][0])] # take 1. element of '2-' => 2 and 2 * (-1) => -2 is index of a list
                elif dict_mark["mark"].isdigit():
                    dict_mark["mark"] = int(dict_mark["mark"])
                else:
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

            average = 0
            if weight_sum != 0:
                average = round(mark_times_weight / weight_sum, 2)
            else:
                logger.warning(f"{subject} has no average weight is (0)")
            subjects[subject].append({"avg": average})

            # Export marks to json file
            export_json(subjects, JSON_OUTPUT_PATH)

            logger.info("Calculating completed successfully")

        except Exception as e:
            logger.exception(f"Something happened during processing marks: {e}")
            return {}

    logger.info("Subject will sorted and returned")
    return dict(sorted(subjects.items()))
