# Measures your internet speed on speedtest.net
# Then logs in on Twitter and complains if the internet is too slow ^^
# github.com/Promethium147 on 2024-02-06

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument("--start-maximized")

TEST_TIME = 45

MAX_DOWN = 250
MAX_UP = 30

PROMISED_DOWN = 125
PROMISED_UP = 30

PROVIDER = "@xxxxxxx"

CHROME_DRIVER_PATH = "C:\\chromedriver"
TWITTER_USERNAME = "xxxxxxx"
TWITTER_PASSWORD = "xxxxxxx"


class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")

        time.sleep(3)

        # Deny cookies
        deny_button = self.driver.find_element(By.ID, "onetrust-reject-all-handler")
        deny_button.click()

        time.sleep(2)

        go_button = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()

        # Wait for the test to be done, adjust to your best values
        time.sleep(TEST_TIME)

        # Close the 50-billion tests popup
        billion_close = self.driver.find_element(By.CSS_SELECTOR, ".close-btn.pure-button.pure-button-primary")
        billion_close.click()

        time.sleep(2)

        # Extract the speed values
        self.down = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.up = self.driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

    def tweet_at_provider(self):

        self.driver.get("https://twitter.com/i/flow/login")

        time.sleep(2)

        # Enter username
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(TWITTER_USERNAME)
        WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='username']"))).send_keys(Keys.ENTER)

        time.sleep(2)

        # Enter password
        WebDriverWait(self.driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(TWITTER_PASSWORD)
        WebDriverWait(self.driver, 20).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, "input[autocomplete='current-password']"))).send_keys(Keys.ENTER)

        time.sleep(7)

        # Do a few calculations
        down_number = float(self.down)
        up_number = float(self.up)

        promised_percent_down = round((down_number/PROMISED_DOWN) * 100, 2)
        promised_percent_up = round((up_number/PROMISED_UP) * 100, 2)

        max_percent_down = round((down_number/MAX_DOWN) * 100, 2)
        max_percent_up = round((up_number/MAX_UP) * 100, 2)

        if down_number < PROMISED_DOWN or up_number < PROMISED_UP:
            tweet = (f"Current Internet-Speed: {self.down} Down / {self.up} Up. "
                     f"That is {max_percent_down}% of maximum Down and {max_percent_up}% of maximum Up and {promised_percent_down}% of guaranteed Down. "
                     f"Provider: {PROVIDER}")
            textbox = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.CSS_SELECTOR, '.notranslate')))
            textbox.send_keys(tweet)
            # Send Enter to confirm your provider in the popup
            textbox.send_keys(Keys.RETURN)

            send_button = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/span/span')))
            send_button.click()

            time.sleep(1)

            # Close that "Got it" Popup
            got_it_button = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH, '//*[@id="layers"]/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[3]/div/div')))
            got_it_button.click()

            time.sleep(10)

        self.driver.quit()


bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()
