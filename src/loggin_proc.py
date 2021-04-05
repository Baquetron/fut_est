from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

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
        driver = webdriver.Chrome("../tools/bin/chromedriver.exe", options=options)
    # driver.get("file:///Users/inigo/Sandbox/fut_est/data/transfers_history.html")
    driver.get(r"C:\Users\jjsan\Documents\Git Futmondo\fut_est\data\transfers_history.html")
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
    # table.to_csv('Path where to save data', index=False)



if __name__ == "__main__":
    execute()