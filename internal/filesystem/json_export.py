import json
import logging
import os
from pathlib import Path

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

    # Get path
    project_root = Path(__file__).resolve().parent.parent # Absolut path
    output_path = project_root / name

    # Export
    logger.info("Exporting...")

    try:
        json.dumps(subjects, indent=4, sort_keys=False)
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4)
    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")
        return False

    logger.info("Exporting was successfully finished")

    return True