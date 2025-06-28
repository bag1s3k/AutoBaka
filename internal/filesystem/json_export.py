import json
import logging
import os
from internal.utils.paths_constants import JSON_OUTPUT_PATH

from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def export_json(subjects, name) -> bool:
    """
    Export marks to marks.json
    Args:
        dict of marks
    Returns:
        Boolean: successful or not
    """

    logger.info(f"Current directory: {os.getcwd()}")

    if not subjects:
        logger.warning("Nothing in subjects")
        return False

    # Export
    logger.info("Exporting...")

    if not JSON_OUTPUT_PATH:
        logger.error("Json output path is empty")
        return False

    try:
        json.dumps(subjects, indent=4, sort_keys=False)
        with open(JSON_OUTPUT_PATH, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4)
    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")
        return False

    logger.info("Exporting was successfully finished")

    return True