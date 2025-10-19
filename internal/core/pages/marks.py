import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode

from ..page_model import BasePage
from internal.utils.decorators import validate_output
from internal.utils.logging_setup import setup_logging


setup_logging()
logger = logging.getLogger(__name__)


class Marks(BasePage):
    """ Inherits from BasePage
        Use for get marks"""
    def __init__(self, driver):
        super().__init__(driver)
        self._subjects = {}

    @validate_output(
        error_msg="Getting marks failed",
        success_msg="Getting marks successful",
        level="error"
    )
    def scrape(self) -> dict[str, list[dict[str, str]]]:
        """ Specific logic to get marks
            :return: empty dict if fail otherwise filled dict"""
        logger.info("Looking for an element on page with marks")

        if not (marks_line := self._find_item(target=(By.XPATH,
                                                    "//tbody//tr[//td "
                                                    "and contains(@class, 'dx-row') "
                                                    "and contains(@class, 'dx-data-row') "
                                                    "and contains(@class, 'dx-row-lines')]"),
                                     mult=True)):
            logger.error(f"Marks not found url")
            return self._subjects

        for single_line in marks_line:
            if not (subject := self._find_item(target=(By.TAG_NAME, "td"), parent=single_line, mult=True)):
                logger.warning("No subject")
                return self._subjects

            mark = subject[1].text
            topic = unidecode(subject[2].text)
            weight = subject[5].text
            date = subject[6].text
            subject_name = unidecode(subject[0].text)

            logger.info(f"Extracting: {mark} {topic} {weight} {date} {subject_name}")

            self._subjects.setdefault(subject_name, []).append({
                "mark": mark,
                "topic": topic,
                "weight": weight,
                "date": date
            })

        return self._subjects


    @validate_output(
        error_msg="Processing marks failed or there are no marks",
        success_msg="Processing marks successful",
        level="error"
    )
    def process_marks(self) -> bool:
        """ Specific logit to process marks
            :return _subjects: sorted dict of processed marks"""

        if not self._subjects: return False

        logger.info(f"Processing marks")

        # (1- -> 1.5) or N don't add to the list and Calculate average
        text_to_num = [4.5, 3.5, 2.5, 1.5]
        for subject, list_subject in self._subjects.items():
            logger.info(f"Processing subject: {subject}")
            try:
                marks = []
                for dict_mark in list_subject:
                    if "-" in dict_mark["mark"]:
                        dict_mark["mark"] = text_to_num[-int(dict_mark["mark"][0])]  # take 1. char of '2-' => 2 and 2 * (-1) => -2 is index of a list (text_to_num)
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

                self._subjects[subject].append({"avg": average})

            except Exception as e:
                logger.error(f"Something happened during processing marks: {e}")
                return False

        self._subjects = dict(sorted(self._subjects.items()))

        return True


    @property
    def subjects(self):
        """Getter"""
        return self._subjects