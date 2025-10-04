import logging
import json
import os

from internal.utils.decorators import validate_output

logger = logging.getLogger(__name__)


@validate_output("Exporting failed or it's empty", "Exported successfully completed", "warning")
def export_results(subjects, path) -> bool:
    """
    Export averages to file
    :param subjects: dict of marks
    :param path: path to output file
    :return bool: True on success False otherwise
    """

    if not subjects: return False

    try:
        with open(path, "w") as file:
            for subject, marks in subjects.items():
                file.write(f"{subject:30} {marks[-1]["avg"]}\n")
        return True
    except Exception as e:
        logger.exception(f"Issue during exporting: {e}")
        return False


@validate_output("Exporting failed or nothing to export", "Exporting successful", "warning")
def export_json(item, path) -> bool:
    """
    Export marks to JSON file
    :param item: dict of marks
    :param path: absolut file path
    :return bool: True if successful, False otherwise
    """

    logger.info(f"Current directory: {os.getcwd()}")

    if not item:
        return False

    # Export
    logger.info("Exporting json...")

    if not path:
        logger.error("Wrong export json path")
        return False

    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump(item, file, indent=4, ensure_ascii=False)
        return True

    except Exception as e:
        logger.exception(f"Something happened during exporting: {e}")
        return False