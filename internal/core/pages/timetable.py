from datetime import datetime
import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode

from ..page_model import BasePage
from internal.utils.decorators import validate_output
from internal.utils.logging_setup import setup_logging
from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import RAW_TIMETABLE_OUTPUT

setup_logging()
logger = logging.getLogger(__name__)


class Timetable(BasePage):
    """ Inherits BasePage
        Use for get timetable (in code is used shortcut TT or tt for timetable)"""

    def __init__(self, driver):
        super().__init__(driver)
        self.NORMAL_TT_DAYS = "//div[@class='day-row normal']"
        self.NORMAL_TT_DATES = ".//div/div/div/div/span"
        self.NORMAL_TT_LECTURES = ("./div/div/span/div/div[@class='empty']" # Free lecture
                                   " | ./div/div/span/div/div/div[@class='top clearfix']" # Non-lecture
                                   " | ./div/div/span/div/div/div/div[2]" # Lecture
                                   " | ./div/div/div[2]/div") # Free day
        self.NEXT_TT_BTN = '//*[@id="cphmain_linkpristi"]'
        self.PERMANENT_TT_BTN = '//*[@id="cphmain_linkpevny"]'
        self.PERMANENT_TT_DAYS = "//div[@class='day-row double']"

        self.timetable = {}
        self.odd_timetable = {}
        self.even_timetable = {}

    @validate_output(
        error_msg="Extracting timetable failed",
        success_msg="Extracting timetable successful",
        level="error"
    )
    def _extract_tt(self, days_xpath, date_xpath=None, lectures_xpath=None, dual=False) -> dict:
        """Specific logic to get specific timetable
            :param days_xpath:
            :param date_xpath:
            :param lectures_xpath:
            :return: Empty dict if fail otherwise filled dict"""
        if not (days := self._find_item((By.XPATH, days_xpath), mult=True)):
            return self.timetable

        if n_days := len(days) != 5:
            logger.debug(f"Wrong amount of days: {n_days} there must be 5")

        which_day = 0  # 0 stands for Monday...
        for day in days:
            lectures = []

            # ------- SINGLE TT ------ #
            if not dual:
                if not (date_webelement := self._find_item((By.XPATH, date_xpath), parent=day)):
                    return self.timetable
                datetime_formats = [
                    "%d/%m",
                    "%d.%m."
                ]
                date = None
                for date_format in datetime_formats:
                    try:
                        date = datetime.strptime(f"{date_webelement.text}", date_format)
                    except:
                        continue
                date = datetime(datetime.now().year, date.month, date.day)

                if not(lectures_webelement := self._find_item((By.XPATH, lectures_xpath), parent=day, mult=True)):
                    return self.timetable
                lectures = [unidecode(i.text) for i in lectures_webelement]

            # ------- DUAL TT ------- #
            else:
                date = which_day
                which_day += 1
                if not (double_lectures := self._find_item((By.XPATH, ".//div/div/span/div"), parent=day, mult=True)):
                    return self.timetable

                for single_lectures in double_lectures:
                    if not (double_lecture := self._find_item(
                        (By.XPATH, ".//div[@class='empty'] | .//div/div/div[2]"),
                        parent=single_lectures,
                        mult=True
                    )):
                        return self.timetable

                    lectures_to_string = [unidecode(t.text) for t in double_lecture]
                    for i, x in enumerate(lectures_to_string[:]):
                        if i % 2 == 0: lectures_to_string.remove(x)

                    lectures.append(lectures_to_string)

            # Fill dict
            if not dual:
                date = date.date().isoformat()
            self.timetable[date] = []
            for lecture in lectures:
                self.timetable[date].append(lecture)

            # One day of timetable should have 10 lessons
            if (ntimetable := len(self.timetable[date])) != 10:
                logger.debug(f"Wrong amount of lectures: {ntimetable} there must be 10")

        return self.timetable

    @staticmethod
    def _delete_empty(dct: dict):
        """Delete empty lists in the dictionary
        :param dct: processed dictionary"""
        for k, v in list(dct.items()):
            if not v:
                dct.pop(k)

    @validate_output(
        error_msg="Processing timetable failed",
        success_msg="Processing successful",
        level="error"
    )
    def _process_timetable(self):
        """Create dictionary of timetable for current week, next week, odd week, even week
        :return: Empty dict if fail otherwise filled dict for a month in advance"""
        even, odd, current2weeks = {}, {}, {}
        for day, lectures in self.timetable.items():
            even[day] = []
            odd[day] = []
            current2weeks[day] = []

            for lecture in lectures:
                if not isinstance(lecture, list):
                    current2weeks[day].append(lecture)
                    continue
                if not lecture:
                    even[day].append('')
                    odd[day].append('')
                else:
                    for even_or_odd in lecture:
                        if even_or_odd.startswith("S"): # 'S' stands for even
                            even[day].append(even_or_odd[3:])
                        else:
                            odd[day].append(even_or_odd[3:])

        self._delete_empty(even)
        self._delete_empty(odd)
        self._delete_empty(current2weeks)

        self.timetable = current2weeks
        self.odd_timetable = odd
        self.even_timetable = even

        export_json(odd, "C:\\Users\\mate1\\Downloads\\odd.json")
        export_json(even, "C:\\Users\\mate1\\Downloads\\even.json")
        export_json(current2weeks, "C:\\Users\\mate1\\Downloads\\current2weeks.json")

        return self.timetable

    def scrape(self):
        """ It's help func, it calls other functions (extract_tt or find_item)
            :return: true if successful otherwise None"""
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        if tmp := self._find_item((By.XPATH, self.NEXT_TT_BTN)):
            tmp.click()
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        if tmp := self._find_item((By.XPATH, self.PERMANENT_TT_BTN)):
            tmp.click()
        if self.timetable:
            self._extract_tt(
                days_xpath=self.PERMANENT_TT_DAYS,
                dual=True
            )
        export_json(self.timetable, RAW_TIMETABLE_OUTPUT)
        self._process_timetable()