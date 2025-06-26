import json
import logging
import os

from config.logging_conf import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def export_json(subjects) -> bool:
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
    output_path = os.path.join("autobaka", "marks.json")

    # Export
    logger.info("Exporting...")

    try:
        subjects_json = json.dumps(subjects, indent=4, sort_keys=False)
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(subjects, file, indent=4)
    except Exception as e:
        logger.exception(f"Something happened during exporting: {str(e)}")

    logger.info("Exporting was successfully finished")

    return True