import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode
from datetime import datetime, timedelta

from ..page_model import BasePage
from internal.utils.logging_setup import setup_logging
from internal.utils.decorators import validate_output
from internal.filesystem.ini_loader import config
from internal.utils.lecture_dict import short

setup_logging()
logger = logging.getLogger(__name__)

class Absence(BasePage):
    """ Inherits BasePage
        Use for get absence"""
    def __init__(self, driver):
        super().__init__(driver)
        
        self.absence = []
        self.counts = {}

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
                "subject": short(unidecode(subject_str[0])),
                "passed_lectures": int(subject_str[1]),
                "absence": int(subject_str[2]),
                "%": subject_str[3]
            })

        return self.absence

    @validate_output(
        error_msg="No lectures in counts",
        level="error"
    )
    def calc_lectures(self, timetable: dict, even: dict, odd: dict) -> dict:
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
        for lectures in timetable.values():
            for lecture in lectures:
                if not lecture or len(lecture) > 4:
                    continue
                if lecture in self.counts:
                    self.counts[lecture] += 1
                else:
                    self.counts[lecture] = 1

        return self.counts

    @validate_output(
        error_msg="Calculating absence failed",
        level="error"
    )
    def calc_absence(self):
        for subject in self.absence:
            self.counts[subject["subject"]] += subject["passed_lectures"]
            subject["%"] = round(subject["absence"] / self.counts[subject["subject"]], 2)

        # user_absence = input("Enter your absence in format: 1.1.2025 8:00 - 1.1.2025 13:00").split(":")[1]
        # user_absence.split("-")

        t_start = "11.11.2025 8:59"
        t_end = "11.11.2025 12:33"

        lecture_time = [
            {"7:10": "7:55"},
            {"8:00": "8:45"},
            {"8:55": "9:40"},
            {"10:00": "10:45"},
            {"10:55": "11:40"},
            {"11:50": "12:35"},
            {"12:45": "13:30"},
            {"13:40": "14:25"},
            {"14:35": "15:20"},
            {"15:30": "16:15"}
        ]

        converter_lectures = []
        for lecture in lecture_time:
            for start_time, end_time in lecture.items():
                start = datetime.strptime(start_time, "%H:%M")
                end = datetime.strptime(end_time, "%H:%M")
                converter_lectures.append((start, end))
                # print(k,v)

        t_start = datetime.strptime(t_start, "%d.%m.%Y %H:%M")
        t_end = datetime.strptime(t_end, "%d.%m.%Y %H:%M")

        found_indices = set()
        for index, (start, end) in enumerate(converter_lectures):
            if start.time() <= t_start.time() <= end.time() and timedelta(minutes=15) < t_start - start: # todo: amount of minutes from config
                found_indices.add(index)

            if start.time() <= t_end.time() <= end.time() and timedelta(minutes=15) < t_end - start:
                found_indices.add(index)

            if t_start.time() <= start.time() and end.time() <= t_end.time():
                found_indices.add(index)