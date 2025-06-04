from selenium.webdriver.common.by import By
import time

def login(driver, username, password):
    driver.get("https://bakaweb.cichnovabrno.cz/login")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "login").click()

def navigate_to_marks(driver):
    time.sleep(3)
    driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikace").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "ico32-modul-klasifikacePrubezna").click()
    time.sleep(2)
    driver.find_element(By.ID, "cphmain_linkchronologicky").click()
    time.sleep(1)