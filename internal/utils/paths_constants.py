from pathlib import Path

def find_project_root(target_folder: str = "autobaka") -> Path:
    """
    This func finds project root folder
    Returns:
        - absolute path of the project root
    """
    path = Path(__file__).resolve() # get current absolut path of this file

    while path.name != target_folder:
        if path.parent == path: # protection against infinite loop
            return Path()
        path = path.parent

    return path

PROJECT_ROOT = find_project_root()
CONFIG_PATH = PROJECT_ROOT / "config" / "config.ini"
LOG_PATH = PROJECT_ROOT / "output" / "project_log.log"
ENV_PATH = PROJECT_ROOT / "config" / ".env"