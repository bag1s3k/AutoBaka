import logging
import json
import os

from internal.utils.decorators import log_message
from internal.utils.var_validator import log_variable

logger = logging.getLogger(__name__)


@log_message("Exporting failed", "Exported successfully completed", "warning")
def export_results(subjects, path) -> bool:
    """
    Export averages to file
    :param subjects: dict of marks
    :param path: path to output file
    :return bool: True on success False otherwise
    """

    log_variable(subjects, "warning", "Nothing to export")

    try:
        with open(path, "w") as file:
            for subject, marks in subjects.items():
                file.write(f"{subject:30} {marks[-1]["avg"]}\n")
        return True
    except Exception as e:
        logger.exception(f"Issue during exporting: {str(e)}")
        return False


@log_message("Exporting failed", "Exporting successful", "warning")
def export_json(subjects, path) -> bool:
    """
    Export marks to JSON file
    :param subjects: dict of marks
    :param path: absolut file path
    :return bool: True if successful, False otherwise
    """

    logger.info(f"Current directory: {os.getcwd()}")

    if not log_variable(subjects,
                        level="warning",
                        error_message="No subjects to export",
                        right_message="Exporting successful"):
        return False

    # Export
    logger.info("Exporting json...")

    if not log_variable(path, level="critical", error_message="Wrong path"):
        return False

    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4, ensure_ascii=False)
        return True

    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")
        return False