import os
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    username = os.getenv("BAKA_USERNAME")
    password = os.getenv("BAKA_PASSWORD")

    return username, password