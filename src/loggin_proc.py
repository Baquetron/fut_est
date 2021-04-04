from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

_FUTMONDO_ADDRESS = "https://www.futmondo.com/"

def execute():
    tranfer_list_scrapping()

def tranfer_list_scrapping():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("../tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../tools/bin/chromedriver", options=options)

    driver.get("file:///Users/inigo/Sandbox/fut_est/data/transfers_history.html")
    # check transfer history list is visible
    elem_transfer_history = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pressReleases"]')))
    # get all elems from list
    l_transfer_history = driver.find_elements_by_css_selector("#pressReleases > ul > li > ul")
 
    for i, row in enumerate(l_transfer_history):
        line = str(row.text)
        print(line)

if __name__ == "__main__":
    execute()