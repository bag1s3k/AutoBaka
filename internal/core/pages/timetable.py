from datetime import datetime, timedelta
import logging

from selenium.webdriver.common.by import By

from ..page_model import BasePage
from internal.filesystem.ini_loader import config
from internal.utils.decorators import validate_output
from internal.utils.logging_setup import setup_logging
from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import TIMETABLE_OUTPUT

setup_logging()
logger = logging.getLogger(__name__)


class Timetable(BasePage):
    """
    Inherits BasePage
    Use for get timetable (in code is used shortcut TT or tt for timetable)
    """

    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.NORMAL_TT_DAYS = "//div[@class='day-row normal']"
        self.NORMAL_TT_DATES = ".//div/div/div/div/span"
        self.NORMAL_TT_LECTURES = (".//div/div/span/div/div[@class='empty']"
                                   " | .//div/div/span/div/div/div[@class='top clearfix']"
                                   " | .//div/div/span/div/div/div/div[2]")
        self.NEXT_TT_BTN = '//*[@id="cphmain_linkpristi"]'
        self.PERMANENT_TT_BTN = '//*[@id="cphmain_linkpevny"]'
        self.PERMANENT_TT_DAYS = "//div[@class='day-row double']"

        self.SEMESTER_END = datetime.strptime(config.get_auto_cast("DATES", "semester1_end"), "%Y-%m-%d").date()
        self.timetable = {}

    @validate_output(
        error_msg="Extracting timetable failed",
        success_msg="Extracting timetable successful",
        level="error"
    )
    def _extract_tt(self, days_xpath, date_xpath=None, lectures_xpath=None, last_date=None, dual=False) -> dict:
        """
        Specific logic to get specific timetable
        :param days_xpath:
        :param date_xpath:
        :param lectures_xpath:
        :param last_date:
        :return: Empty dict if fail otherwise filled dict
        """
        days = self._find_items((By.XPATH, days_xpath))

        if n_days := len(days) != 5:
            logger.debug(f"Wrong amount of days: {n_days} there must be 5")

        which_day = 1  # 1 stands for Monday...
        for day in days:
            year: int = datetime.now().year
            lectures = []

            # ------- SINGLE TT ------ #
            if not dual:
                date_webelement = self._find_item((By.XPATH, date_xpath), parent=day)
                date = datetime.strptime(f"{date_webelement.text}/{year}", "%d/%m/%Y")
                lectures_webelement = self._find_items((By.XPATH, lectures_xpath), parent=day)
                lectures = [i.text for i in lectures_webelement]

            # ------- DUAL TT ------- #
            else:
                skip_weekend = datetime.strptime(str(f"{last_date}"), "%Y-%m-%d") + timedelta(days=2)
                date = skip_weekend + timedelta(days=which_day)
                which_day += 1

                double_lectures = self._find_items((By.XPATH, ".//div/div/span/div"), parent=day)

                for single_lectures in double_lectures:
                    double_lecture = self._find_items(
                        (By.XPATH, ".//div[@class='empty'] | .//div/div/div[2]"),
                        parent=single_lectures)
                    lectures_to_string = [t.text for t in double_lecture]
                    for i, x in enumerate(lectures_to_string[:]):
                        if i % 2 == 0: lectures_to_string.remove(x)

                    lectures.append(lectures_to_string)

            # Fill dict
            date = date.date().isoformat()
            self.timetable[date] = []
            for lecture in lectures:
                self.timetable[date].append(lecture)

            # One day of timetable should have 10 lessons
            if (n_timetable := len(self.timetable[date])) != 10:
                logger.debug(f"Wrong amount of lectures: {n_timetable} there must be 10")

        export_json(self.timetable, TIMETABLE_OUTPUT)
        return self.timetable


    def get_tt(self):
        """
        It's help func, it calls other functions (extract_tt or find_item)
        :return: true if successful otherwise None
        """
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.NEXT_TT_BTN)).click()
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.PERMANENT_TT_BTN)).click()
        self._extract_tt(
            days_xpath=self.PERMANENT_TT_DAYS,
            last_date=list(self.timetable.keys())[-1],  # last key is the last date
            dual=True
        )