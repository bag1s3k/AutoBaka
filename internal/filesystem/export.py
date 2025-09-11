import logging

from internal.utils.decorators import log_message
from internal.utils.var_validator import log_variable

logger = logging.getLogger(__name__)

@log_message("Exporting failed", "Exported successfully completed", "warning")
def export_results(subjects, path):
    """
    Export averages to file
    Args:
        subjects: dict of marks
        path: path to output file
    Returns:
        bool
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