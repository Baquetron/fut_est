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
_PLAYER_SCORES_PAGE = "file:///Users/inigo/Sandbox/fut_est/data/payer_score_page.html"

def parse_json(filepath):
    with open(filepath, "r") as f:
        dictionary = json.load(f)
        return dictionary

def get_player_scores(filepath):
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("../tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../tools/bin/chromedriver", options=options)

    driver.get(_PLAYER_SCORES_PAGE)
    elem_player_scores = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="matches"]')))
    elems_scores = driver.find_elements_by_css_selector('#matches > div > div.game')
    scores_l = len(elems_scores)
    for i, elem in enumerate(elems_scores):
        show_more_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="matches"]/div[' + str(i+1) + ']/div[2]/div[2]/strong')))
        driver.execute_script("arguments[0].scrollIntoView(true);",show_more_button)
        val =elem.find_element_by_xpath('//*[@id="matches"]/div[' + str(i+1) + ']/div[2]/div[2]/strong')
        print(val.text)


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
    get_player_scores(_PLAYER_SCORES_PAGE)

if __name__ == "__main__":
    execute()