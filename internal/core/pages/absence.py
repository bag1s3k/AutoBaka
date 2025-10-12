import logging

from selenium.webdriver.common.by import By
from unidecode import unidecode

from ..page_model import BasePage
from internal.utils.logging_setup import setup_logging
from internal.utils.decorators import validate_output

setup_logging()
logger = logging.getLogger(__name__)

class Absence(BasePage):
    """ Inherits BasePage
        Use for get absence"""
    def __init__(self, driver):
        super().__init__(driver)
        
        self._absence = []

    @validate_output(
        error_msg="Absence failed",
        success_msg="Absence successful",
        level = "warning"
    )
    def scrape(self) -> list:
        """ Specific logic to get absence
            :return: empty list if fail otherwise filled list"""
        if not (subjects := self._find_item((By.XPATH, "//tr[@class='dx-row dx-data-row']"), mult=True)):
            return self._absence
        for subject in subjects:
            if not (subjects_l := self._find_item((By.XPATH, "td"), parent=subject, mult=True)):
                return self._absence
            subject_str = [t.text for t in subjects_l]

            self._absence.append({
                "subject": unidecode(subject_str[0]),
                "passed_lectures": int(subject_str[1]),
                "absence": int(subject_str[2]),
                "%": subject_str[3]
            })

        return self._absence
    
    @property
    def absence(self):
        """getter"""
        return self._absence