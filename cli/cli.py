from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_loader import set_env
from main import run
import logging

setup_logging()
logger = logging.getLogger(__name__)

def config() -> bool:
    """
    Setup app using CLI and commands
    """

    status = None

    while True:
        command = input("root/config> ")

        if command == "login-details":
            username = input("username: ").strip()
            password = input("password: ").strip()

            # Successful?
            if not set_env("BAKA_USERNAME", username) or not set_env("BAKA_PASSWORD", password):
                print("Setting failed")
                logger.error("Writing to .env failed")
                status = False
            else:
                print(" Successfully overwrite")
                status = True
        elif command == "settings":
            pass
        elif command == "help":
            pass
        elif command == "exit":
            return status
        else:
            logger.warning(f"Unknown command: {command}")
            print(f"Unknown command: {command}, write 'help'")
            continue

    return True

def run_app_loop() -> bool:
    """
    Main loop function, it's infinite loop until user enter "exit"
    """

    status = None

    while True:
        try:
            command = input("root> ").strip().lower()
            logger.info(f"Command choice: {command} ")

            if command == "config":
                status = config()
            elif command == "help":
                print("config: configuration of app\nhelp: help menu\nrun: run main app (get averages)\nshow: show results\ndev: developer mode\nexit: exit app")
            elif command == "run":
                status = run("cli")
            elif command == "show":
                pass
            elif command == "dev":
                pass
            elif command == "exit":
                return status
            else:
                logger.warning(f"Unknown command: {command}")
                print(f"Unknown command: {command}, write 'help'")
                continue

        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return status

if __name__ == "__main__":
    run_app_loop()

