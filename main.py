from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json
from unidecode import unidecode

# options = Options()
# options.add_experimental_option("detach", True)
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
#                           options=options)
#
# driver.get("https://bakaweb.cichnovabrno.cz/login")
#
# with open("data.txt", "r", encoding="utf-8-sig") as file:
#     username = file.readline().strip()
#     password = file.readline().strip()
#
# # Logging
# driver.find_element(By.NAME, "username").send_keys(username)
# driver.find_element(By.NAME, "password").send_keys(password)
# driver.find_element(By.NAME, "login").click()
#
# # Navigation to marks
# time.sleep(3)
# driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikace").click()
# time.sleep(1)
# driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikacePrubezna").click()
# time.sleep(2)
# driver.find_element(By.ID, "cphmain_linkchronologicky").click()
# time.sleep(1)
#
# # Get marks
# marks_line = driver.find_elements("xpath", "//tbody//tr[.//td and contains(@class, 'dx-row') and contains(@class, 'dx-data-row') and contains(@class, 'dx-row-lines')]")
#
# subjects = {}
#
# for single_line in marks_line:
#     subject = single_line.find_elements(By.TAG_NAME, "td")
#
#     mark = subject[1].text
#     topic = unidecode(subject[2].text)
#     weight = subject[5].text
#     date = subject[6].text
#     subject_name = unidecode(subject[0].text)
#
#     subjects.setdefault(subject_name, []).append({
#         "mark": mark,
#         "topic": topic,
#         "weight": weight,
#         "date": date
#     })
#
# subjectsJSON = json.dumps(subjects, indent=4, sort_keys=False)
#
# with open("marks.json", "w") as file:
#     file.write(subjectsJSON)

with open("marks.json", "r") as file:
    subjects = json.load(file)

for subject, list_subject in subjects.items():
    marks = []
    for dict_mark in list_subject:
        marks.append(tuple([dict_mark["mark"], dict_mark["weight"]]))

    for mark in marks:
        print(mark)