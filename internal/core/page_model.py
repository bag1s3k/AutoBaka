import logging
from datetime import datetime, timedelta
from typing import Tuple
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from unidecode import unidecode

from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import JSON_RAW_OUTPUT_PATH
from internal.utils.decorators import log_message
from internal.utils.var_validator import log_variable
from internal.filesystem.ini_loader import config
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class BasePage(ABC):
    def __init__(self, driver, url, timeout=config.get_auto_cast("SETTINGS", "timeout")):
        self.driver = driver
        self.timeout = timeout
        self.url = url

    @log_message(error_message="Moving to target page failed url: {self.url}",
                 right_message="Moving to target page successful",
                 level="critical")
    def get(self):
        """Move to target page"""
        try:
            self.driver.get(self.url)
            return True
        except Exception as e:
            logger.critical(f"Issue while moving to targe page: {self.url}")
            logger.exception(e)
            return False

    @log_message(error_message="Item not found",
                 right_message="Item found",
                 level="critical")
    def find_item(self, target: Tuple[str, str], parent=None):
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_element_located(target))
            return item
        except Exception as e:
            logger.exception(e)
            return None

    @log_message(error_message="Items not found",
                 right_message="Items found",
                 level="critical")
    def find_items(self, target: Tuple[str, str], parent=None):
        if parent is None:
            parent = self.driver

        try:
            item = WebDriverWait(parent, self.timeout).until(
                ec.presence_of_all_elements_located(target))
            return item
        except Exception as e:
            logger.exception(e)
            return None

    @staticmethod
    def check_output(self): pass


class Login(BasePage):

    @log_message(error_message="Login failed",
                 right_message="Login successful",
                 level="critical")
    def login(self, username, password):
        try:
            # Find required elements on website (username and password field, login button)
            username_field = self.find_item(target=(By.NAME, "username"))
            password_field = self.find_item(target=(By.NAME, "password"))
            login_button = self.find_item(target=(By.NAME, "login"))

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
    def get_marks(self):
        try:
            logger.info("Looking for an element on page with marks")

            marks_line = self.find_items(target=(By.XPATH,
                                                       "//tbody//tr[//td "
                                                        "and contains(@class, 'dx-row') "
                                                        "and contains(@class, 'dx-data-row') "
                                                        "and contains(@class, 'dx-row-lines')]"))

            # Load whole marks (date, mark, value...) it's line of these data
            if not log_variable(marks_line,
                                level="warning",
                                error_message=f"Marks not found url: {self.driver.current_url} title: {self.driver.title}",
                                right_message=f"Marks found url {self.driver.current_url} title: {self.driver.title}"):
                return {}


            subjects = {}
            for single_line in marks_line:
                subject = self.find_items(target=(By.TAG_NAME, "td"), parent=single_line)

                if not log_variable(subject,
                                    level="warning",
                                    error_message="No subject",
                                    right_message="Subject found"):
                    return {}

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

            # Export marks to json file
            export_json(subjects, JSON_RAW_OUTPUT_PATH)

            return subjects

        except Exception as e:
            logger.exception({str(e)})
            return {}

class Timetable(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver, url)
        self.NORMAL_TT_DAYS = "//div[@class='day-row normal']"
        self.NORMAL_TT_DATES = ".//div/div/div/div/span"
        self.NORMAL_TT_LECTURES = ".//div/div/span/div/div[@class='empty'] | .//div/div/span/div/div/div[@class='top clearfix'] | .//div/div/span/div/div/div/div[2]"

        self.NEXT_TT_BTN = '//*[@id="cphmain_linkpristi"]'

        self.PERMANENT_TT_BTN = '//*[@id="cphmain_linkpevny"]'
        self.PERMANENT_TT_DAYS = "//div[@class='day-row double']"
        self.PERMANENT_TT_LECTURES = "//div/div/div/span/div/div[@class='empty'] | //div/div/div/span/div/div/div/div[2]"

        self.timetable = {}
        semester_end = datetime.strptime(config.get_auto_cast("DATES", "semester1_end"), "%Y-%m-%d").date()
        today = datetime.today().date()

        self.difference = (semester_end - today).days

        for _ in range(self.difference):
            today = today + timedelta(days=1)
            self.timetable[today.isoformat()] = ""

    @log_message(error_message="Extracting timetable failed",
                 right_message="Extracting timetable successful",
                 level="error")
    def get_timetable(self):

        def extract_tt(days_xpath, date_xpath, lectures_xpath, last_date=None):

            try:
                days = self.find_items((By.XPATH, days_xpath))

                if n_days := len(days) != 5:
                    logger.debug(f"Wrong amount of days: {n_days} there must be 5")

                for day in days:
                    if date_xpath is not None:
                        date = self.find_item((By.XPATH, date_xpath), parent=day)
                        date = date.text
                    else:
                        year = datetime.now().year
                        last_date = datetime.strptime(str(f"{last_date}/{year}"), "%m/%d/%Y")
                        date = last_date + timedelta(days=1)
                        last_date = date = date.strftime("%#m/%#d/%#Y")

                    lectures = self.find_items((By.XPATH, lectures_xpath), parent=day)

                    self.timetable[date] = []
                    for lecture in lectures:
                        self.timetable[date].append(lecture.text)

                    if (n_timetable := len(self.timetable[date])) != 10:
                        logger.debug(f"Wrong amount of lectures: {n_timetable} there must be 10")

            except Exception as e:
                logger.exception(f"Something unexcepted happened: {e}")

        extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self.find_item((By.XPATH, self.NEXT_TT_BTN)).click()
        extract_tt(self.NORMAL_TT_DAYS, self.NORMAL_TT_DATES, self.NORMAL_TT_LECTURES)
        self.find_item((By.XPATH, self.PERMANENT_TT_BTN)).click()
        extract_tt(days_xpath=self.PERMANENT_TT_DAYS,
                   date_xpath=None,
                   lectures_xpath=self.PERMANENT_TT_LECTURES,
                   last_date="10/10")

        # temp print
        def print_week(week):
            for k, v in week.items():
                print(k, v)

        print_week(self.timetable)