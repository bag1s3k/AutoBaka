from core.selenium_setup import setup_driver
from config.env_loader import load_credentials
from core.navigation import login
from core.marks_processor import get_marks, process_marks
from utils.export import export_results
from config.config_manager import get_config

def main():
    driver = setup_driver()
    username, password = load_credentials()

    login(driver, username, password)

    processed_marks = process_marks(get_marks(driver))

    export_results(processed_marks, get_config())

    driver.quit()

if __name__ == "__main__":
    main()