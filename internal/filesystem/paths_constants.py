from pathlib import Path

from internal.utils.decorators import validate_output

@validate_output(error_msg="No project root found", success_msg="Project root found", level="error")
def find_project_root(target_folder: str = "autobaka") -> Path:
    """Find project root folder
        :return path: absolute path of the project root"""
    path = Path(__file__).resolve() # get current absolut path of this file

    while path.name != target_folder:
        if path.parent == path: # protection against infinite loop
            return Path()
        path = path.parent

    return path

PROJECT_ROOT = find_project_root()
INI_PATH = PROJECT_ROOT / "config" / "config.ini"
ENV_PATH = PROJECT_ROOT / "config" / ".env"
LOG_PATH = PROJECT_ROOT / "output" / "log" / "project_log.log"
MARKS_OUTPUT = PROJECT_ROOT / "output" / "marks" / "marks.json"
RAW_MARKS_OUTPUT = PROJECT_ROOT / "output" / "marks" / "raw_marks.json"
TIMETABLE_OUTPUT = PROJECT_ROOT / "output" / "timetable" / "timetable.json"
RAW_ABSENCE_OUTPUT = PROJECT_ROOT / "output" / "absence" / "raw_absence.json"
ABSENCE_OUTPUT = PROJECT_ROOT / "output" / "absence" / "absence.json"