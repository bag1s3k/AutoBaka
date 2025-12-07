from pathlib import Path
from internal.utils.decorators import validate_output

PROJECT_ROOT = Path(__file__).parent
INI_PATH = PROJECT_ROOT / "config" / "config.ini"
ENV_PATH = PROJECT_ROOT / "config" / ".env"
LOG_PATH = PROJECT_ROOT / "output" / "log" / "project_log.log"
MARKS_OUTPUT = PROJECT_ROOT / "output" / "marks" / "processed_marks.json"
RAW_MARKS_OUTPUT = PROJECT_ROOT / "output" / "marks" / "raw_marks.json"
TIMETABLE_OUTPUT = PROJECT_ROOT / "output" / "timetable" / "two_weeks_timetable.json"
RAW_TIMETABLE_OUTPUT = PROJECT_ROOT / "output" / "timetable" / "raw_timetable.json"
RAW_ABSENCE_OUTPUT = PROJECT_ROOT / "output" / "absence" / "raw_absence.json"
ABSENCE_OUTPUT = PROJECT_ROOT / "output" / "absence" / "absence.json"
class PathConfig:

    def __init__(self):
        # Root is always parent of this file
        self._root: Path = Path(__file__).parent

    @property
    @validate_output(error_msg="Root directory doesn't exist", level="critical")
    def ROOT(self) -> Path | bool:
        return self._root

    @property
    @validate_output(error_msg="Config file doesn't exist", level="critical")
    def ini(self):
        return self._root / "config" / "config.ini"

    # levels INFO are there because that files are optional,
    # e.g. in case user use CLI to enter login details (argparse)
    # or if the file is needed, it will be created
    @property
    @validate_output(error_msg="Env file doesn't exist", level="info")
    def env(self):
        return self._root / "config" / ".env"

    @property
    @validate_output(error_msg="Log file doesn't exist", level="info")
    def log(self):
        return self._root / "output" / "config" / "project_log.log"

    @property
    @validate_output(error_msg="File with processed marks doesn't exist", level="info")
    def processed_marks(self):
        return self._root / "output" / "marks" / "processed_marks.json"

    @property
    @validate_output(error_msg="File with raw marks doesn't exist", level="info")
    def raw_marks(self):
        return self._root / "output" / "marks" / "raw_marks.json"

    @property
    @validate_output(error_msg="File with timetable of current two weeks doesn't exist", level="info")
    def two_weeks_timetable(self):
        return self._root / "output" / "timetable" / "two_weeks_timetable.json"

    @property
    @validate_output(error_msg="File with raw timetable doesn't exist", level="info")
    def raw_timetable(self):
        return self._root / "output" / "timetable" / "raw_timetable.json"

    @property
    @validate_output(error_msg="File with calculated absence doesn't exist", level="info")
    def calculated_absence(self):
        return self._root / "output" / "absence" / "absence.json"

    @property
    @validate_output(error_msg="File with raw absence doesn't exist", level="info")
    def raw_absence(self):
        return self._root / "output" / "absence" / "raw_absence.json"

PATHS = PathConfig()