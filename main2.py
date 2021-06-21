import requests
from pprint import pprint
import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from data import API_URL
from data import USERNAME
from data import PASSWORD
from data import TWITER_URL


class TwitterBot:

    def __init__(self):
        self.response = requests.get(API_URL)
        self.chrome_driver_path = 'C:\\Development\\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.chrome_driver_path)
        self.data = self.response.json()['cases_time_series']
        self.today = dt.date.today()
        self.yesterday = self.today - dt.timedelta(days=1)
        self.stats = ''
        self.tweet = ''

    def get_data(self):

        for day in self.data:
            if day["dateymd"] == str(self.yesterday):
                self.stats = day
        date = self.stats["date"]
        confirmed_cases = self.stats["dailyconfirmed"]
        confirmed_deaths = self.stats["dailydeceased"]
        confirmed_recoveries = self.stats["dailyrecovered"]

        self.tweet = f" Date: {date}\n Number of confirmed cases today: {confirmed_cases}\n Number of confirmed deaths today:" \
                     f" {confirmed_deaths}\n Number of confirmed recoveries: {confirmed_recoveries}."

        print(self.tweet)

    def twitter_login(self):

        self.driver.get(TWITER_URL)
        sleep(2)
        email_input = self.driver.find_element_by_name('session[username_or_email]')
        password_input = self.driver.find_element_by_name('session[password]')
        email_input.send_keys(USERNAME)
        password_input.send_keys(PASSWORD)
        sleep(1)
        password_input.send_keys(Keys.ENTER)

    def tweet_data(self):

        sleep(2)
        tweet_input = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
        tweet_input.click()
        tweet_input.send_keys(self.tweet)
        tweet_button = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        tweet_button.click()

        sleep(1)
        self.driver.quit()
