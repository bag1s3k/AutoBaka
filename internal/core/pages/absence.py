import logging

from selenium.webdriver.common.by import By

from ..page_model import BasePage
from internal.filesystem.export import export_json
from internal.filesystem.paths_constants import RAW_ABSENCE_OUTPUT
from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class Absence(BasePage):
    """
    Inherits BasePage
    Use for get absence
    """
    def __init__(self, driver, url):
        super().__init__(driver, url)

        self.absence = []

    def get_absence(self):
        """
        Specific logic to get absence
        :return: empty dict if fail otherwise filled dict
        """
        subjects = self._find_items((By.XPATH, "//tr[@class='dx-row dx-data-row']"))
        for subject in subjects:
            subjects_l = self._find_items((By.XPATH, "td"), parent=subject)
            subject_str = [t.text for t in subjects_l]

            self.absence.append({
                "subject": subject_str[0],
                "passed_lectures": int(subject_str[1]),
                "absence": int(subject_str[2]),
                "%": subject_str[3]
            })

        export_json(self.absence, RAW_ABSENCE_OUTPUT)

        return self.absence