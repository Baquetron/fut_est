from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from datetime import date, timedelta

_FUTMONDO_ADDRESS = "https://www.futmondo.com/"


def execute():
    # tranfer_list_scrapping()
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
    elem_transfer_history = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="pressReleases"]')))
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
    # driver.get(r"C:\Users\jjsan\Documents\Git Futmondo\fut_est\data\player_historic_price.html")
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
    # Clicking on the button to ensure that I am an adult
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@class="infoBox"]/div/div/a[2]'))).click()
    # Accessing to the Squad Players in order to check the market players
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="userChampionships"]')))
    squad_link = driver.find_element_by_xpath('//*[@id="userChampionships"]/ul/div[2]/div/div[5]/a[1]')
    squad_link.click()
    # Wait until the players in the right side menu are displayed
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="players"]')))
    # Displaying all the players by their name
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="sortPlayers"]')))
    displaying_all_players = driver.find_element_by_xpath('//*[@id="sortPlayers"]/li[1]')
    displaying_all_players.click()
    time.sleep(1)
    # Iterating through all the players included in the market
    WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
        (By.XPATH, '//*[@id="players"]')))

    # Retrieving all the players included in the current page
    pages = 0
    players_name = []
    end_date = date.today()
    last_date = date(2021, 5, 25)
    date_difference = end_date - last_date
    players_price = []
    players_price_date = []
    while True:
        if pages == 0:
            pass
        else:
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  driver.find_element_by_xpath('//*[@class="paginationContainer"]/ul/li[4]'))
            time.sleep(1)
            # This code allows us to catch when the button to change of players page
            # is no longer available. When the exception is caught a break condition
            # is executed to go out of the loop.
            try:
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@class="icon-arrow-right"]'))).click()
            except:
                # When no more players are available for being scrapped the program
                # goes out of the loop.
                print("Exception has been caught-> No more players are available")
                break

        players = driver.find_elements_by_xpath('//*[@id="players"]/section/ul')
        for player_number in range(1, 6): #len(players) + 1):
            # Declaration of the list that will be used to include the different dates containing
            # the prices of the players
            date_points = []
            # Script that needs to be executed in order to display all the players and obtain their information.
            # It basically scrolls down the player list until displaying the required element
            driver.execute_script("arguments[0].scrollIntoView(true);",
                                  driver.find_element_by_xpath('//*[@id="players"]/section/ul[{}]'.format(player_number)))
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="players"]/section/ul[{}]'.format(player_number))))
            # Save players name in a list
            players_name.append(driver.find_element_by_xpath('//*[@id="players"]/section/ul[{}]'.format(player_number))
                                .find_element_by_css_selector('li > strong').text)
            player_click = driver.find_element_by_xpath('//*[@id="players"]/section/ul[{}]'.format(player_number))\
                .find_element_by_css_selector('li > img')
            player_click.click()
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@class="playerWindow"]/div[4]/div[1]'))).click()
            # Retrieving the player charts information
            # Retrieve charts info
            url_data = driver.current_url
            driver.get(url_data)
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="playerSummaryPricesChart"]')))
            y_Cord = driver.execute_script("return Highcharts.charts[0].series[0].yData")
            # Here we obtain the number of days from the first price value until the one obtained
            # the 25/05/2021
            delta_dates = timedelta(len(y_Cord)) - date_difference
            # Generating the list containing the points associated to the prices
            date_points = [str(last_date - timedelta(days=i)) for i in range(delta_dates.days - 1, -1, -1)]
            players_price_date.append("; ".join(date_points))
            # Save the players price in a string separated by ; and a space
            players_price.append("; ".join([str(i) for i in y_Cord[0:len(date_points):1]]))
            driver.back()
            time.sleep(0.5)
            WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(
                (By.XPATH, '//*[@id="players"]')))
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="sortPlayers"]/li[1]'))).click()
            time.sleep(0.5)
            # This will allow us to go to the next player page, note that, when going
            # back to the default page it always display the first page of the list. This
            # loop is needed to retrieve the information of the players included in the following
            # pages.
            for i in range(pages):
                driver.execute_script("arguments[0].scrollIntoView(true);",
                                      driver.find_element_by_xpath('//*[@class="paginationContainer"]/ul/li[4]'))
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@class="icon-arrow-right"]'))).click()
        pages += 1

    # TODO. Create the csv file for including the players name. Create the DB to
    # include the players price.


if __name__ == "__main__":
    execute()
