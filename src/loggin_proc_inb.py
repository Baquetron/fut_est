from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import pandas as pd

_JSON_FILE = "../conf/user_data_inb.json"
_FUTMONDO_ADDRESS = "https://www.futmondo.com/"
_LOCAL_TRANSFER_LIST = "file:///Users/inigo/Sandbox/fut_est/data/futmondo_transfer_list_full.html"

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

    driver.get(_LOCAL_TRANSFER_LIST)
    # check transfer history list is visible
    elem_transfer_history = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="pressReleases"]')))
    # get all elems from list
    l_transfer_history = driver.find_elements_by_css_selector("#pressReleases > ul > li > ul")
    # Extracting information for each of the transfers
    players = []
    times = []
    amounts = []
    sellers = []
    buyers = []
    for i, row in enumerate(l_transfer_history):
        transfer_player = row.find_element_by_css_selector('li.text > strong')
        transfer_time = row.find_element_by_css_selector('li.text > time')
        transfer_amount = row.find_element_by_css_selector('li.text > span')
        users = row.find_elements_by_css_selector('div.from > strong')
        players.append(transfer_player.text)
        times.append(transfer_time.text)
        amounts.append(transfer_amount.text)
        sellers.append(users[0].text)
        buyers.append(users[1].text)

    # Creating DataFrame with the transfer's information
    table = pd.DataFrame({'Transfer Time': times, 'Player': players,
                          'Transfer amount': amounts, 'Seller': sellers,
                          'Buyer': buyers}, index=range(1, len(players) + 1))
    # Saving the data in .csv format
    table.to_csv('../data/transfer_history.csv', index=False)

def execute():
    loggin_page()

if __name__ == "__main__":
    loggin_page()