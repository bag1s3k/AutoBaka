from pathlib import Path
from internal.utils.decorators import validate_output


@validate_output(error_msg="No project root found", success_msg="Project root found", level="error")
def find_project_root(target_folder: str = "autobaka") -> Path:
    """
    It finds project root folder
    :return path: absolute path of the project root
    """
    path = Path(__file__).resolve() # get current absolut path of this file

    while path.name != target_folder:
        if path.parent == path: # protection against infinite loop
            return Path()
        path = path.parent

    return path

PROJECT_ROOT = find_project_root()
INI_PATH = PROJECT_ROOT / "config" / "config.ini"
LOG_PATH = PROJECT_ROOT / "output" / "project_log.log"
ENV_PATH = PROJECT_ROOT / "config" / ".env"
JSON_OUTPUT_PATH = PROJECT_ROOT / "output" / "marks.json"
JSON_RAW_OUTPUT_PATH = PROJECT_ROOT / "output" / "raw_marks.json"