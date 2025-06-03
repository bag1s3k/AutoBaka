from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from unidecode import unidecode
from configparser import ConfigParser

# Setup
options = Options()
options.add_experimental_option("detach", False)

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

subjects = {}

for single_line in marks_line:
    subject = single_line.find_elements(By.TAG_NAME, "td")

    mark = subject[1].text
    topic = unidecode(subject[2].text)
    weight = subject[5].text
    date = subject[6].text
    subject_name = unidecode(subject[0].text)

    subjects.setdefault(subject_name, []).append({
        "mark": mark,
        "topic": topic,
        "weight": weight,
        "date": date
    })

# Calculate marks
for subject, list_subject in subjects.items():
    marks = []
    for dict_mark in list_subject:
        if "-" in dict_mark["mark"]:
            text_to_num = [4.5, 3.5, 2.5, 1.5]
            dict_mark["mark"] = dict_mark["mark"][::-1]
            dict_mark["mark"] = text_to_num[int(dict_mark["mark"])]
        elif not dict_mark["mark"].isdigit():
            continue

        marks.append([dict_mark["mark"], dict_mark["weight"]])

    mark_times_weight = 0
    weight_sum = 0

    for mark in marks:
        mark_times_weight += float(mark[0]) * float(mark[1])
        weight_sum += float(mark[1])

    average = str(mark_times_weight / weight_sum)[:4]
    subjects[subject].append({"avg": average})

# Sort
subjects = dict(sorted(subjects.items()))


# Export
config = ConfigParser()
with open('config.ini', 'r', encoding='utf-8') as f:
    config.read_file(f)

path = config.get("PATHS", "result_path")

with open(path, "w") as file:
    for subject, marks in subjects.items():
        file.write(f"{subject:30} {marks[-1]["avg"]}\n")