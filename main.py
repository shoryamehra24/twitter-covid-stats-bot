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

chrome_driver_path = 'C:\\Development\\chromedriver.exe'


# Using COVID API to extract yesterday's data
response = requests.get(API_URL)
data = response.json()['cases_time_series']

today = dt.date.today()
yesterday = today - dt.timedelta(days=1)

stats = ''

for day in data:
    if day["dateymd"] == str(yesterday):
        stats = day

date = stats["date"]
confirmed_cases = stats["dailyconfirmed"]
confirmed_deaths = stats["dailydeceased"]
confirmed_recoveries = stats["dailyrecovered"]

tweet = f" Date: {date}\n Number of confirmed cases today: {confirmed_cases}\n Number of confirmed deaths today:" \
        f" {confirmed_deaths}\n Number of confirmed recoveries: {confirmed_recoveries}."

print(tweet)

# Initiating Selenium driver
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(TWITER_URL)
sleep(2)

# Twitter Login
email_input = driver.find_element_by_name('session[username_or_email]')
password_input = driver.find_element_by_name('session[password]')
email_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
sleep(1)
password_input.send_keys(Keys.ENTER)

# Tweeting Data
sleep(2)
tweet_input = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/label/div[1]/div/div/div/div/div[2]/div/div/div/div')
tweet_input.click()
tweet_input.send_keys(tweet)
tweet_button = driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
tweet_button.click()


