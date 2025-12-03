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
    def calc_absence(self, timetable: dict):
        for subject in self.absence:
            self.counts[subject["subject"]] += subject["passed_lectures"]
            subject["%"] = round((subject["absence"] / self.counts[subject["subject"]]) * 100, 2)

        LECTURE_TIME_RANGE = {
            "7:10": "7:55",
            "8:00": "8:45",
            "8:55": "9:40",
            "10:00": "10:45",
            "10:55": "11:40",
            "11:50": "12:35",
            "12:45": "13:30",
            "13:40": "14:25",
            "14:35": "15:20",
            "15:30": "16:15"
        }

        absence_from = datetime.strptime("2025-12-04 08:00", "%Y-%m-%d %H:%M") # TODO: user input
        absence_to = datetime.strptime("2025-12-04 13:30", "%Y-%m-%d %H:%M") # TODO: user input

        missed = {}

        lecture_starts = list(LECTURE_TIME_RANGE.keys())
        lecture_ends = list(LECTURE_TIME_RANGE.values())

        for day_str, subjects in timetable.items():
            day_date = datetime.strptime(day_str, "%Y-%m-%d")

            # Skip passed days
            if day_date + timedelta(hours=23, minutes=59) < absence_from:
                continue

            for idx, subject in enumerate(subjects):
                if subject == "":
                    continue

                start_time_str = lecture_starts[idx]
                end_time_str = lecture_ends[idx]

                lect_start = datetime.strptime(f"{day_str} {start_time_str}", "%Y-%m-%d %H:%M")
                lect_end = datetime.strptime(f"{day_str} {end_time_str}", "%Y-%m-%d %H:%M")

                if not absence_to <= lect_start or absence_from >= lect_end:
                    missed[subject] = missed.get(subject, 0) + 1

        return missed
