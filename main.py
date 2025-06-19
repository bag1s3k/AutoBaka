from core import setup_driver, login, get_marks, process_marks
from config import load_credentials, get_config, setup_logging
from utils import export_results

setup_logging()

driver = setup_driver()
username, password = load_credentials()

login(driver, username, password)

processed_marks = process_marks(get_marks(driver))

export_results(processed_marks, get_config())

driver.quit()