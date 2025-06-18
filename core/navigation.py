from selenium.webdriver.common.by import By
import time

def login(driver, username, password):
    driver.get("https://bakaweb.cichnovabrno.cz/login")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "login").click()
    time.sleep(2)
    driver.get("https://bakaweb.cichnovabrno.cz/next/prubzna.aspx?s=chrono")
    time.sleep(1)