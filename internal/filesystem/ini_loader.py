from internal.filesystem.paths_constants import INI_PATH
import configparser

config = configparser.ConfigParser()
config.read(INI_PATH, "utf-8")

def read_config():
    for section in config.sections():
        print(f"[{section}]")
        for k, v in config[section].items():
            print(f"{k} = {v}")

        print()