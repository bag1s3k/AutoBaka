from pathlib import Path
import logging

from logging_setup import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

def find_project_root(target_folder: str = "autobaka") -> Path:
    """
    This func finds project root folder
    Returns:
        - absolute path of the project root
    """
    path = Path(__file__).resolve() # get current absolut path of this file
    logger.info("Get current absolut path of this file")

    logger.info("")
    while path.name != target_folder:
        if path.parent == path: # protection against infinite loop
            logger.error(f"Root folder: {target_folder} not found")
            return Path()
        path = path.parent

    logger.info(f"Root folder: {path} successfully found")
    return path

PROJECT_ROOT = find_project_root()

CONFIG_PATH = PROJECT_ROOT / "config.ini"
LOG_PATH = PROJECT_ROOT / "project_log.log"