import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode
from datetime import datetime, timedelta

from ..page_model import BasePage
from internal.utils.logging_setup import setup_logging
from internal.utils.decorators import validate_output
from internal.filesystem.ini_loader import config

setup_logging()
logger = logging.getLogger(__name__)

class Absence(BasePage):
    """ Inherits BasePage
        Use for get absence"""
    def __init__(self, driver):
        super().__init__(driver)
        
        self.absence = []

    @validate_output(
        error_msg="Absence failed",
        success_msg="Absence successful",
        level = "warning"
    )
    def scrape(self) -> list:
        """ Specific logic to get absence
            :return: empty list if fail otherwise filled list"""
        if not (subjects := self._find_item((By.XPATH, "//tr[@class='dx-row dx-data-row']"), mult=True)):
            return self.absence
        for subject in subjects:
            if not (subjects_l := self._find_item((By.XPATH, "td"), parent=subject, mult=True)):
                return self.absence
            subject_str = [t.text for t in subjects_l]

            self.absence.append({
                "subject": unidecode(subject_str[0]),
                "passed_lectures": int(subject_str[1]),
                "absence": int(subject_str[2]),
                "%": subject_str[3]
            })

        return self.absence

    @staticmethod
    @validate_output(
        error_msg="No lectures in counts",
        level="error"
    )
    def calc_lectures(timetable: dict, even: dict, odd: dict) -> dict:
        # TODO: EXCLUDE HOLIDAYS ATD, AUTO CALC END OF SEMESTER
        """ Calculate amount of each lecture to end of semester
            :param timetable: Current 2 weeks timetable
            :param even: Even timetable
            :param odd: Odd timetable
            :return: Amount of each lecture to end of semester"""
        today = datetime.today()
        end = datetime.strptime(config.get_auto_cast("DATES", "semester1_end"), "%Y-%m-%d")
        sub = end - today
        day = today.date()

        # Remove passed dates
        for k in list(timetable.keys()):
            if datetime.strptime(str(day), "%Y-%m-%d") > datetime.strptime(k, "%Y-%m-%d"):
                timetable.pop(k)

        # Create whole timetable from today to end of the semester
        for _ in range(sub.days):
            if timetable.get(str(day), 0) == 0:
                if day.weekday() not in [5, 6]:
                    if day.isocalendar().week % 2 == 0:
                        timetable[str(day)] = even[day.weekday()]
                    else:
                        timetable[str(day)] = odd[day.weekday()]
            day += timedelta(days=1)

        # Get remaining lectures
        counts = {}
        for lectures in timetable.values():
            for lecture in lectures:
                if not lecture or len(lecture) > 4:
                    continue
                if lecture in counts:
                    counts[lecture] += 1
                else:
                    counts[lecture] = 1

        return counts