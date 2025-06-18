import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(levelname)-8s %(asctime)s - %(name)s - %(message)s",
        datefmt="%d.%m.%Y %H:%M:%S",
        handlers=[
            logging.FileHandler("project_log.log"),
            logging.StreamHandler()
        ]
    )

setup_logging()