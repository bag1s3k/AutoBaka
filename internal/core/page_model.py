import logging
from datetime import datetime, timedelta
from typing import Tuple
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from unidecode import unidecode

from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import JSON_RAW_OUTPUT_PATH, JSON_OUTPUT_PATH
from internal.utils.decorators import validate_output
from internal.filesystem.ini_loader import config
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class BasePage(ABC):
    """
    Abstract base class for using selenium (generally every interact with website)
    - every subclass is specific for 1 interaction (e.g. class Login)
    """
    def __init__(self, driver, url, timeout=config.get_auto_cast("SETTINGS", "timeout")):
        self.driver = driver
        self.timeout = timeout
        self.url = url

    @validate_output(error_msg=f"Moving to the target page failed url",
                     success_msg=f"Moving to the target page successful url:",
                     level="critical")
    def get(self):
        """Move to target page"""
        try:
            self.driver.get(self.url)
            return True
        except Exception as e:
            logger.exception(e)
            return False

    @validate_output(error_msg="Item on website not found",
                 success_msg="Item on website found",
                 level="warning")
    def _find_item(self, target: Tuple[str, str], parent=None) -> WebElement | None:
        """
        Find specific element on website
        :param target: tuple selenium expression e.g (By.XPATH, "//div")
        :param parent: Selenium WebElement; default self.driver If None
        :return item: If true return matching element otherwise return None
        """
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_element_located(target))
            return item
        except Exception as e:
            logger.warning(e)
            return None

    @validate_output(error_msg="Items not found",
                 success_msg="Items found",
                 level="warning")
    def _find_items(self, target: Tuple[str, str], parent=None) -> list[WebElement] | None:
        """
        Find specific elements on website
        :param target: tuple selenium expression e.g (By.XPATH, "//div")
        :param parent: Selenium WebElement; default self.driver If None
        :return item: If true return matching elements otherwise return None
        """
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_all_elements_located(target))
            return item
        except Exception as e:
            logger.exception(e)
            return None


class Login(BasePage):
    """
    Inherits from BasePage
    Use for login
    """

    @validate_output(error_msg="Login failed",
                 success_msg="Login successful",
                 level="critical")
    def login(self, username, password) -> bool:
        """
        Specific login logic
        :param username: username (string)
        :param password: password (string)
        :return: True if successful otherwise False
        """
        try:
            # Find required elements on website (username and password field, login button)
            username_field = self._find_item(target=(By.NAME, "username"))
            password_field = self._find_item(target=(By.NAME, "password"))
            login_button = self._find_item(target=(By.NAME, "login"))

            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            login_button.click()

            return True

        except Exception as e:
            logger.exception(e)
            return False


class MarksPage(BasePage):
    """
    Inherits from BasePage
    Use for get marks
    """
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.SUBJECTS = {}

    @validate_output(error_msg="Getting marks failed",
                 success_msg="Getting marks successful",
                 level="critical")
    def get_marks(self) -> dict[str, list]:
        """
        Specific logic to get marks
        :return: if not empty dict successful otherwise empty dict
        """
        try:
            logger.info("Looking for an element on page with marks")

            marks_line = self._find_items(target=(By.XPATH,
                                                       "//tbody//tr[//td "
                                                        "and contains(@class, 'dx-row') "
                                                        "and contains(@class, 'dx-data-row') "
                                                        "and contains(@class, 'dx-row-lines')]"))

            # Load whole marks (date, mark, value...) it's line of these data
            if not marks_line:
                logger.error(f"Marks not found url: {self.driver.current_url} title: {self.driver.title}")
                self.SUBJECTS = {}
                return self.SUBJECTS

            for single_line in marks_line:
                subject = self._find_items(target=(By.TAG_NAME, "td"), parent=single_line)

                if not subject:
                    logger.warning("No subject")
                    self.SUBJECTS = {}
                    return self.SUBJECTS

                mark = subject[1].text
                topic = unidecode(subject[2].text)
                weight = subject[5].text
                date = subject[6].text
                subject_name = unidecode(subject[0].text)

                logger.info(f"Extracting: {mark} {topic} {weight} {date} {subject_name}")

                self.SUBJECTS.setdefault(subject_name, []).append({
                    "mark": mark,
                    "topic": topic,
                    "weight": weight,
                    "date": date
                })

            # Export marks to json file
            export_json(self.SUBJECTS, JSON_RAW_OUTPUT_PATH)

            return self.SUBJECTS

        except Exception as e:
            logger.exception(e)
            self.SUBJECTS = {}
            return self.SUBJECTS

    @validate_output(error_msg="Processing marks failed or there are no marks",
                     success_msg="Processing marks successful",
                     level="error")
    def process_marks(self) -> dict[str, list]:
        """
        Specific logit to process marks

        :return subjects: sorted dict of processed marks
        """

        if not self.SUBJECTS: return self.SUBJECTS

        logger.info(f"Processing marks")

        # (1- -> 1.5) or N don't add to the list and Calculate average
        text_to_num = [4.5, 3.5, 2.5, 1.5]
        for subject, list_subject in self.SUBJECTS.items():
            logger.info(f"Processing subject: {subject}")
            try:
                marks = []
                for dict_mark in list_subject:
                    if "-" in dict_mark["mark"]:
                        dict_mark["mark"] = text_to_num[-int(dict_mark["mark"][
                                                                 0])]  # take 1. char of '2-' => 2 and 2 * (-1) => -2 is index of a list (text_to_num)
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

                self.SUBJECTS[subject].append({"avg": average})

                # Export marks to json file
                export_json(self.SUBJECTS, JSON_OUTPUT_PATH)

            except Exception as e:
                logger.exception(f"Something happened during processing marks: {e}")
                return {}

        self.SUBJECTS = dict(sorted(self.SUBJECTS.items()))
        return  self.SUBJECTS


class Timetable(BasePage):
    """
    Inherits BasePage
    Use for get timetable (in code is used shortcut TT or tt for timetable
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
        self.PERMANENT_TT_LECTURES = ".//div/div/span/div/div[@class='empty'] | .//div/div/span/div/div/div/div[2]"

        self.SEMESTER_END = datetime.strptime(config.get_auto_cast("DATES", "semester1_end"), "%Y-%m-%d").date()
        self.timetable = {}

    def _extract_tt(self, days_xpath, date_xpath, lectures_xpath, last_date=None) -> bool:
        """
        Specific logic to get specific timetable
        :param days_xpath:
        :param date_xpath:
        :param lectures_xpath:
        :param last_date:
        :return: True if successful otherwise False
        """
        try:
            days = self._find_items((By.XPATH, days_xpath))

            if n_days := len(days) != 5:
                logger.debug(f"Wrong amount of days: {n_days} there must be 5")

            n = 3
            for day in days:
                year = datetime.now().year

                # If None, use calculated date otherwise use date from website
                if date_xpath is not None:
                    date_raw = self._find_item((By.XPATH, date_xpath), parent=day)
                    date_raw = datetime.strptime(f"{date_raw.text}/{year}", "%d/%m/%Y")
                else:
                    new_last_date = datetime.strptime(str(f"{last_date}"), "%Y-%m-%d")
                    date_raw = new_last_date + timedelta(days=n)
                    n += 1

                lectures = self._find_items((By.XPATH, lectures_xpath), parent=day)

                # skip Sat, Sun
                if date_raw.weekday() in [6, 7]:
                    continue

                date = date_raw.date().isoformat()
                self.timetable[date] = []
                for lecture in lectures:
                    self.timetable[date].append(lecture.text)

                # One day of timetable should have 10 lessons
                if (n_timetable := len(self.timetable[date])) != 10:
                    logger.debug(f"Wrong amount of lectures: {n_timetable} there must be 10")

            return True

        except Exception as e:
            logger.exception(f"Something unexcepted happened: {e}")
            return False


    # TODO: CHECK OUTPUT !!!
    def get_timetable(self):
        """
        It's help func, it calls other functions (extract_tt or find_item)
        :return: true if successful otherwise None
        """
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.NEXT_TT_BTN)).click()
        self._extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self._find_item((By.XPATH, self.PERMANENT_TT_BTN)).click()
        self._extract_tt(days_xpath=self.PERMANENT_TT_DAYS,
                   date_xpath=None,
                   lectures_xpath=self.PERMANENT_TT_LECTURES,
                   last_date="2025-10-10")