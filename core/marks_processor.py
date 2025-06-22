import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode
from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def get_marks(driver):
    """
    Extraction marks from baka page
    Args:
        driver: instance of the browser
    Returns:
        dict: dictionary {subject: average}
    """
    marks_line = driver.find_elements("xpath",
                                      "//tbody//tr[.//td and contains(@class, 'dx-row') and contains(@class, 'dx-data-row') and contains(@class, 'dx-row-lines')]")

    subjects = {}

    for single_line in marks_line:
        subject = single_line.find_elements(By.TAG_NAME, "td")

        mark = subject[1].text
        topic = unidecode(subject[2].text)
        weight = subject[5].text
        date = subject[6].text
        subject_name = unidecode(subject[0].text)

        subjects.setdefault(subject_name, []).append({
            "mark": mark,
            "topic": topic,
            "weight": weight,
            "date": date
        })

    return subjects

def process_marks(subjects):
    for subject, list_subject in subjects.items():
        marks = []
        for dict_mark in list_subject:
            if "-" in dict_mark["mark"]:
                text_to_num = [4.5, 3.5, 2.5, 1.5]
                dict_mark["mark"] = dict_mark["mark"][::-1]
                dict_mark["mark"] = text_to_num[int(dict_mark["mark"])]
            elif not dict_mark["mark"].isdigit():
                continue

            marks.append([dict_mark["mark"], dict_mark["weight"]])

        mark_times_weight = 0
        weight_sum = 0

        for mark in marks:
            mark_times_weight += float(mark[0]) * float(mark[1])
            weight_sum += float(mark[1])

        average = str(mark_times_weight / weight_sum)[:4]
        subjects[subject].append({"avg": average})

    return dict(sorted(subjects.items()))