from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

_FUTMONDO_ADDRESS = "https://www.futmondo.com/"

def execute():
    #tranfer_list_scrapping()
    player_price_scrapping()


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


def player_price_scrapping():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument('disable-infobars')
    try:
        driver = webdriver.Chrome("../tools/bin/gc84/chromedriver.exe", options=options)
    except:
        driver = webdriver.Chrome("../tools/bin/chrome_90.0.4430.24/chromedriver.exe", options=options)
    # driver.get("file:///Users/inigo/Sandbox/fut_est/data/transfers_history.html")
    #driver.get(r"C:\Users\jjsan\Documents\Git Futmondo\fut_est\data\player_historic_price.html")
    driver.get(_FUTMONDO_ADDRESS)
    # Clicking in the logging ("Jugar") button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '/html/body/header/div/div/a[1]'))).click()

    # Selecting the method to login
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((
        By.XPATH, '//*[@id="login"]/div/section/div/div[2]/a/i'))).click()

    # Introducing login information
    user_login = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((
        By.XPATH, '//*[@id="login"]/div/section/div/div/form/div[1]/input')))
    user_login.send_keys("javiersanmartin1995@gmail.com")
    password_login = driver.find_element_by_xpath('//*[@id="login"]/div/section/div/div/form/div[2]/input')
    password_login.send_keys("Sanmartin17")

    # Clicking in the access button
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="login"]/div/section/div/div/a'))).click()

    # Accessing to the Squad Players
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="userChampionships"]')))
    transfer_market_link = driver.find_element_by_xpath('//*[@id="userChampionships"]/ul/div[1]/div/div[6]/a[6]')
    transfer_market_link.click()
    # Wait until the players are displayed
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="teamPlayers"]')))
    # Displaying all the players by their name
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="sortPlayers"]')))
    displaying_all_players = driver.find_element_by_xpath('//*[@id="sortPlayers"]/li[1]')
    displaying_all_players.click()

    # Iterating through all the players included in the market
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="teamPlayers"]')))

    # Retrieving all the players included in the current page
    #TODO. To be completed, currently, it is not working as expected.
    players = driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li')
    for player_number in range(0, len(players) - 1):
        if player_number > 0:
            time.sleep(3)
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="teamPlayers"]')))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="sortPlayers"]/li[1]'))).click()
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="teamPlayers"]')))
        print(len(driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li')))
        player_click = driver.find_elements_by_xpath('//*[@id="teamPlayers"]/ul/li')[player_number]\
            .find_element_by_css_selector('div > figure > img')
        player_click.click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@class="desktopContainer"]/div[5]/div[1]/div[5]/div[1]'))).click()
        # Retrieving the player charts information
        # Retrieve charts info
        url_data = driver.current_url
        driver.get(url_data)
        WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
            (By.XPATH, '//*[@id="playerSummaryPricesChart"]')))
        x_Cord = driver.execute_script("return Highcharts.charts[0].series[0].xData")
        y_Cord = driver.execute_script("return Highcharts.charts[0].series[0].yData")
        print(x_Cord)
        print(y_Cord)
        driver.back()


    time.sleep(10)


    # user_login = WebDriverWait
    # elem_charts = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
    #     By.XPATH, '//*[@id="highcharts-hr8xomy-23"]'))
    # charts = driver.execute_script("return Highcharts.charts[1].series[1].yData")
    # print(type(charts))
    # print(charts)

    # check history price is available
    # elem_price_history = WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
    #     (By.XPATH, '//*[@id="highcharts-20"]')))
    # print(elem_price_history)
    #
    # player_price_history = driver.find_elements_by_css_selector("#highcharts-20 > svg > g.highcharts-series-group > g.highcharts-series")
    # graphs = []
    # for elem in player_price_history:
    #     cord_x = []
    #     cord_y = []
    #     data = elem.find_element_by_tag_name('path').get_attribute('d')
    #     print(data)
    #     values = data[2:len(data) - 1].split(' L ')
    #     for val in values:
    #         coordinates = val.split(" ")
    #         cord_x.append(float(coordinates[0]))
    #         cord_y.append(float(coordinates[1]))
    #     graphs.append([cord_x, cord_y])
    # print(len(graphs))
    # print(len(graphs[0]))
    # i = 0
    # for graph in graphs:
    #     i += 1
    #     table_to_create = pd.DataFrame({'x Coordinates': graph[0], 'y Coordinates': graph[1]}
    #                                    , index=range(1, len(graph[0]) + 1))
    #     # Saving the data in .csv format
    #     table_to_create.to_csv('Graph_{}.csv'.format(i), index=False)


if __name__ == "__main__":
    execute()
