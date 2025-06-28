import logging

from internal.utils.logging_setup import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

def export_results(subjects, path):
    """
    Export averages to file
    Args:
        subjects: dict of marks
        path: path to output file
    Returns:
        bool
    """
    logger.info("Marks are gonna be write down")

    if not subjects:
        logger.warning("Nothing to write")
    try:
        with open(path, "w") as file:
            for subject, marks in subjects.items():
                file.write(f"{subject:30} {marks[-1]["avg"]}\n")
        logger.info("Marks were successfully exported")
        return True
    except Exception as e:
        logger.exception(f"Issue during exporting: {str(e)}")
        return False