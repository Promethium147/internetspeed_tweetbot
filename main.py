# Measures your internet speed on speedtest.net
# Then logs in on Twitter and complains if the internet is too slow ^^
# https://github.com/Promethium147/internetspeed_tweetbot, 2024-03-15

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import time

options = Options()
options.add_argument("--start-maximized")

MAX_DOWN = 250
MAX_UP = 30

PROMISED_DOWN = 125
PROMISED_UP = 5

PROVIDER = "@xxxxxxx"

TWITTER_USERNAME = "xxxxxxxxxxx"
TWITTER_PASSWORD = "xxxxxxxxxxx"

# The delays are not necessary for the function,
# but maybe help to prevent bot detection
BOT_DELAY = 2


class InternetSpeedTwitterBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        # Wait for the cookie popup and click to deny
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))).click()

        # Wait for the start button and click it
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a"))).click()

        time.sleep(4)

        # Find the speed selectors
        down_speed = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.download-speed").text
        up_speed = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.upload-speed").text

        # Wait until the speed values are available
        while down_speed == "—" or up_speed == "—":
            time.sleep(1)
            down_speed = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.download-speed").text
            up_speed = self.driver.find_element(By.CSS_SELECTOR, ".result-data-large.number.result-data-value.upload-speed").text

        self.down = float(down_speed)
        self.up = float(up_speed)

    def calculations(self):

        promised_percent_down = round((self.down/PROMISED_DOWN) * 100, 2)
        promised_percent_up = round((self.up/PROMISED_UP) * 100, 2)

        max_percent_down = round((self.down/MAX_DOWN) * 100, 2)
        max_percent_up = round((self.up/MAX_UP) * 100, 2)

        # If the internet speed is below the promised speed, tweet at the provider
        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            self.tweet_at_provider(promised_percent_up, promised_percent_down, max_percent_up, max_percent_down)
        else:
            print(f"Current Internet-Speed: {self.down} Down / {self.up} Up.\n"
                  f"That is {max_percent_down}% of maximum Down, {max_percent_up}% of maximum Up and\n "
                  f"{promised_percent_down}% of guaranteed Down.\n"
                  f"Complaints to {PROVIDER} are not necessary.\n")

    def tweet_at_provider(self, promised_up, promised_down, max_up, max_down):
        # Only gets called if the internet speed is below the promised speed

        self.driver.get("https://twitter.com/i/flow/login")

        time.sleep(BOT_DELAY)

        # Enter username
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(TWITTER_USERNAME)
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(Keys.ENTER)

        time.sleep(BOT_DELAY)

        # Enter password
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(TWITTER_PASSWORD)
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(Keys.ENTER)

        time.sleep(BOT_DELAY)

        tweet = (f"Current Internet-Speed: {self.down} Down / {self.up} Up. "
                 f"That is {max_down}% of maximum Down and {max_up}% of maximum Up and "
                 f"{promised_down}% of guaranteed Down. "
                 f"Provider: {PROVIDER}")

        textbox = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.notranslate')))
        textbox.send_keys(tweet)

        time.sleep(BOT_DELAY)

        # Send Enter to confirm your provider in the popup
        textbox.send_keys(Keys.RETURN)

        time.sleep(BOT_DELAY)

        send_button = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span')))
        send_button.click()

        # You can close the browser now, but I'll keep it open for a while to see the tweet for debugging purposes
        time.sleep(10)

        self.driver.quit()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.calculations()
