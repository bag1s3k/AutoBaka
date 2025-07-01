from internal.utils.logging_setup import setup_logging
from main import run
import logging

setup_logging()
logger = logging.getLogger(__name__)

def run_app_loop():
    while True:
        try:
            command = input("> ").strip().lower()
            logger.info(f"Command choice: {command} ")

            if command == "config":
                pass
            elif command == "help":
                pass
            elif command == "run":
                run("cli")
            elif command == "show":
                pass
            elif command == "dev":
                pass
            elif command == "exit":
                break
            else:
                logger.warning(f"Unknown command: {command}")
                print(f"Unknown command: {command}, write 'help'")
                continue
        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            break

if __name__ == "__main__":
    run_app_loop()