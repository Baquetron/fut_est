from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json

_JSON_FILE = "../conf/user_data.json"
_FUTMONDO_ADDRESS = "https://www.futmondo.com/"
_LOCAL_TRANSFER_LIST = "file:///Users/inigo/Sandbox/fut_est/data/transfers_history.html"

def parse_json(filepath):
    with open(filepath, "r") as f:
        dictionary = json.load(f)
        return dictionary

def loggin_page():
    d_userdata = parse_json(_JSON_FILE)
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("../tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../tools/bin/chromedriver", options=options)

    driver.get(_FUTMONDO_ADDRESS)
    # jugar button
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/header/div/div/a[1]"))).click()
    # facebook loggin
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login"]/div/section/div/div[1]/a[1]/i'))).click()
    # cookies accept
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]"))).click()
    # enter user id and psd
    e_userid = driver.find_element_by_id('email')
    e_userid.send_keys(d_userdata["fut_loggin"]["user"])
    e_psd = driver.find_element_by_id('pass')
    e_psd.send_keys(d_userdata["fut_loggin"]["psd"])
    WebDriverWait(driver,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="loginbutton"]'))).click()
    time.sleep(10)

def execute():
    loggin_page()

if __name__ == "__main__":
    loggin_page()