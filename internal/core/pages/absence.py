import logging

from selenium.webdriver.common.by import By

from ..page_model import BasePage
from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import RAW_ABSENCE_OUTPUT
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
    def scrape(self):
        """ Specific logic to get absence
            :return: empty dict if fail otherwise filled dict"""
        subjects = self._find_items((By.XPATH, "//tr[@class='dx-row dx-data-row']"))
        for subject in subjects:
            subjects_l = self._find_items((By.XPATH, "td"), parent=subject)
            subject_str = [t.text for t in subjects_l]

            self._absence.append({
                "subject": subject_str[0],
                "passed_lectures": int(subject_str[1]),
                "absence": int(subject_str[2]),
                "%": subject_str[3]
            })

        return self._absence
    
    @property
    def absence(self):
        """getter"""
        return self._absence