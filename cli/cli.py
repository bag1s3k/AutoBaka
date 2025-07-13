from internal.utils.logging_setup import setup_logging
from internal.filesystem.env_loader import set_env, load_credentials_from_file
from internal.filesystem.ini_loader import config as config_file
from main import run

import logging

setup_logging()
logger = logging.getLogger(__name__)

def config():
    """
    Setup app using CLI and commands (infinite loop)
    """

    while True:
        command = input("root/config> ").strip()
        logger.info(f"Command: {command}")

        # if Login details continue with --
        if "login-details" in command:

            # show current login details
            if "--current" in command:
                print(load_credentials_from_file())

            # set new login details
            else:
                username = input("username: ").strip()
                if username == "exit":
                    continue

                password = input("password: ").strip()

                if password == "exit":
                    continue

                # Failed
                if not set_env("BAKA_USERNAME", username) or not set_env("BAKA_PASSWORD", password):
                    print("Setting failed")
                    logger.error("Writing to .env failed")

                # Successful
                else:
                    logger.info("Successfully overwrite")
                    print(" Successfully overwrite")

        # If settings continue with --
        elif "settings" in command:

            # Show current config
            if "--current" in command:
                for section in config_file.config.sections():
                    print(f"[{section}]")
                    for key, value in config_file.config.items(section):
                        print(f"{key}: {value}")

            # Enter new config
            else:
                value = input("Enter: 'section option value': ").split(" ")

                try:
                    if not config_file.set_new(value[0], value[1], value[2]):
                        continue

                    print(f"Set new config: {value}")
                    logger.info(f"Set new config: {value}")

                except Exception as e:
                    logger.warning(f"Unexpected warning: {str(e)}")
                    print(str(e))
                    continue

        elif command == "help":
            print("login-details: set new login details\n"
                  "\tWhen u asked to enter details, u can enter exit to stop\n"
                  "\t--current: option to show current login details\n"
                  "settings: set new settings in .ini file\n"
                  "\tto stop the app enter wrong input\n"
                  "\t--current: option to show current content of the .ini file"
                  "exit: exit from root/config> to root/")
        elif command == "exit":
            break
        else:
            logger.warning(f"Unknown command: {command}")
            print(f"Unknown command: {command}, write 'help'")
            continue

def run_app_loop():
    """
    Main loop function, it's infinite loop until user enter "exit"
    """

    print("""
   _____          __        __________         __            
  /  _  \  __ ___/  |_  ____\______   \_____  |  | _______   
 /  /_\  \|  |  \   __\/  _ \|    |  _/\__  \ |  |/ /\__  \  
/    |    \  |  /|  | (  <_> )    |   \ / __ \|    <  / __ \_
\____|__  /____/ |__|  \____/|______  /(____  /__|_ \(____  /
        \/                          \/      \/     \/     \/ 
    """)

    while True:
        try:
            command = input("> ").strip().lower()
            logger.info(f"Command choice: {command} ")

            if command == "config":
                config()
            elif command == "help":
                print("config: configuration of app\n"
                      "help: help menu\nrun: run main app (get averages)\n"
                      "show: show results\n"
                      "dev: developer mode\n"
                      "exit: exit app")
            elif command == "run":
                 run()
            elif command == "show":
                pass
            elif command == "dev":
                pass
            elif command == "exit":
                return True
            else:
                logger.warning(f"Unknown command: {command}")
                print(f"Unknown command: {command}, write 'help'")
                continue

        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return False

if __name__ == "__main__":
    if run_app_loop():
        logger.info("Program was completed successfully")
    else:
        logger.error("Program was terminated with an error")