import json
import logging
import os
from internal.utils.paths_constants import JSON_OUTPUT_PATH

from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def export_json(subjects) -> bool:
    """
    Export marks to JSON file

    Args:
        subjects: dict of marks

    Returns:
        bool: True if successful, False otherwise
    """

    logger.info(f"Current directory: {os.getcwd()}")

    if not subjects:
        logger.warning("No subjects to export")
        return False

    # Export
    logger.info("Exporting...")

    if not JSON_OUTPUT_PATH:
        logger.error("JSON output path is empty or not set")
        return False

    try:
        with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4, ensure_ascii=False)

        logger.info(f"Data successfully exported to {JSON_OUTPUT_PATH}")
        return True
    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")
        return False