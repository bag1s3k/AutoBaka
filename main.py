from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

options = Options()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

driver.get("https://bakaweb.cichnovabrno.cz/login")

with open("data.txt", "r", encoding="utf-8-sig") as file:
    username = file.readline().strip()
    password = file.readline().strip()

# Logging
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password)
driver.find_element(By.NAME, "login").click()

# Navigation to marks
time.sleep(3)
driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikace").click()
time.sleep(1)
driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikacePrubezna").click()
time.sleep(2)
driver.find_element(By.ID, "cphmain_linkchronologicky").click()
time.sleep(1)

# Get marks
marks_line = driver.find_elements("xpath", "//tbody//tr[.//td and contains(@class, 'dx-row') and contains(@class, 'dx-data-row') and contains(@class, 'dx-row-lines')]")

subject = marks_line[0].find_elements(By.TAG_NAME, "td")

mark = subject[1].text
topic = subject[2].text
weight = subject[5].text
date = subject[6].text
subject_name = subject[0].text
print(f"S: {subject_name}\nM: {mark}\nT: {topic}\nW: {weight}\nD: {date}\nSN: {subject_name}")