import json
import logging
import os

from internal.utils.var_validator import log_variable
from internal.utils.decorators import log_message

logger = logging.getLogger(__name__)

@log_message("Exporting failed", "Exporting successful", "warning")
def export_json(subjects, path) -> bool:
    """
    Export marks to JSON file

    Args:
        subjects: dict of marks
        path: absolut file path

    Returns:
        bool: True if successful, False otherwise
    """

    logger.info(f"Current directory: {os.getcwd()}")

    if not log_variable(subjects, "warning", "No subjects to export", "Exporting successful"):
        return False

    # Export
    logger.info("Exporting json...")

    if not log_variable(path, "critical", "Wrong path"):
        return False

    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4, ensure_ascii=False)
        return True

    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")
        return False