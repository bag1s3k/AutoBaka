from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_loader import set_env, load_credentials_from_file
from internal.filesystem.ini_loader import config as config_file
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
        logger.info(f"Command: {command}")

        if "login-details" in command:
            if "--current" in command:
                print(load_credentials_from_file())
            else:
                username = input("username: ").strip()
                if not username == "exit":
                    password = input("password: ").strip()

                    if password == "exit":
                        status = True
                    else:
                        # Successful?
                        if not set_env("BAKA_USERNAME", username) or not set_env("BAKA_PASSWORD", password):
                            print("Setting failed")
                            logger.error("Writing to .env failed")
                            status = False
                        else:
                            logger.info("Successfully overwrite")
                            print(" Successfully overwrite")
                            status = True
        elif "settings" in command:
            if "--current" in command:
                for section in config_file.config.sections():
                    print(f"[{section}]")
                    for key, value in config_file.config.items(section):
                        print(f"{key}: {value}")
            else:
                value = input("Enter: 'section option value': ").split(" ")

                try:
                    if not config_file.set_new(value[0], value[1], value[2]):
                        return False

                    print(f"Set new config: {value}")
                    logger.info(f"Set new config: {value}")

                except Exception as e:
                    logger.warning(f"Unexpected warning: {str(e)}")
                    print(str(e))
                    continue
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
    if run_app_loop():
        logger.info("Program was completed successfully")
    else:
        logger.error("Program was terminated with an error")

