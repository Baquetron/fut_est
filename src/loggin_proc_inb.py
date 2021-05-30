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
    # Accessing to the Squad Players
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="userChampionships"]')))
    transfer_market_link = driver.find_element_by_xpath('//*[@id="userChampionships"]/ul/div[3]/div/div[5]/a[6]')
    transfer_market_link.click()
    # Wait until the players are displayed
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="teamPlayers"]')))
    time.sleep(3)
    # Displaying all the players by their name
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="sortPlayers"]')))
    displaying_all_players = driver.find_element_by_xpath('//*[@id="sortPlayers"]/li[1]')
    displaying_all_players.click()
    # Iterating through all the players included in the market
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="teamPlayers"]')))
    # Retrieving all the players included in the current page
    players = driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li')
    player_att = driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li[1]')
    player_att_img = driver.find_elements_by_css_selector('div > figure > img')
    time.sleep(1)
    player_att_img.click()

    """for player_number in range(1, len(players)):
        player_att = driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li[' + str(player_number) + ']/div[1]/div[5]/strong')
        player        
        print(player_click.text)"""

    time.sleep(180)

def execute():
    loggin_page()

if __name__ == "__main__":
    loggin_page()