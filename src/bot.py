# python
import logging

# selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.remote_connection import LOGGER as seleniumLogger
from urllib3.connectionpool import log as urllibLogger


class GGBot:
    def __init__(
        self, timeout: int = 10, selenium_debug: bool = False, headless: bool = False
    ):
        """Creates new bot instance that interacts with gg.pl

        :Args:
         - timeout (int): number of seconds before timing out
         - selenium_debug (bool): whether the webdriver should output debug info
         - headless (bool): whether the webdriver should start in headless mode
        """

        options = Options()
        if selenium_debug == False:
            seleniumLogger.setLevel(logging.WARNING)
            urllibLogger.setLevel(logging.WARNING)
            options.add_argument("--log-level=3")
            logging.debug("Running in debug mode")
        elif selenium_debug == True:
            seleniumLogger.setLevel(logging.DEBUG)
            urllibLogger.setLevel(logging.DEBUG)
            logging.debug("Running in selenium debug mode")

        if headless == False:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, timeout)
        logging.info("Succesfully initialized driver")

    def close_consent(self):
        """Close cookie consent modal 

        :Raises:
         - TimeoutException: If dismiss button couldn't be found in time
        """

        logging.info("Closing cookie consent")

        # go to home page
        self.driver.get("https://www.gg.pl/")

        try:
            # find dismiss button and try to click it
            dismiss_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".subscribe_button"))
            )
            dismiss_button.click()
            logging.debug("Clicked dismiss button")

            logging.info("Closed cookie consent")
        except TimeoutException as e:
            logging.erorr("Didn't find dismiss button on website")
            raise e

    def login(self, username: str, password: str):
        """Login to gg with username and password

        :Args:
         - username (str): username used to login to gg
         - password (str): password used to login to gg

        :Returns:
         - bool: indicates whether the login was successful or not
        """

        logging.info("Logging in")

        # go to home page
        home_page = "https://gg.pl/"
        self.driver.get(home_page)
        logging.debug(f"Loaded {home_page}")

        # find and click login button
        signin_button = self.driver.find_element_by_xpath(
            "/html/body/header/div[1]/div/div/div[2]/a[2]"
        )
        signin_button.click()
        logging.debug("Clicked the signin button")

        # wait for login iframe to appear
        # then select it
        login_iframe = self.wait.until(
            EC.element_to_be_clickable(((By.NAME, "login-iframe")))
        )
        logging.debug("Found login iframe")

        # switch to login iframe using id found in the iframe element
        self.driver.switch_to.frame(login_iframe.get_attribute("id"))
        logging.debug("Switched to login iframe")

        # find username field and enter username
        username_input = self.driver.find_element_by_xpath('//*[@id="login_input"]')
        username_input.send_keys(username)
        logging.debug("Entered username")

        # find password field and enter password
        password_input = self.driver.find_element_by_xpath('//*[@id="password"]')
        password_input.send_keys(password)
        logging.debug("Entered password")

        # find login button and click it
        login_button = self.driver.find_element_by_xpath(
            '//*[@id="loginView"]/form/div[4]/button'
        )
        login_button.click()
        logging.debug("Clicked the login button")

        # check if we got redirected to the next page
        if self.driver.current_url.split("/")[0] != "#":
            logging.error("Login failed")
            raise (ValueError("username or password is wrong"))
        else:
            logging.info("Logged in succesfully")

    def start_roulette(self):
        """Starts roulette

        :Returns:
         - bool: indicates whether the roulette was started successfully

        :Raises:
         - NoSuchElementException: If the start button wasn't found
         - TimeoutException: If the div with start button didn't appear
        """

        logging.info("Starting roulette")

        # go to roulette
        roulette_page = "https://www.gg.pl/#roulette"
        self.driver.get(roulette_page)
        logging.debug(f"Loaded {roulette_page}")

        try:
            # for some reason we can't directly access
            # the input tag so we select the parent div
            # and then select it
            start_buttons = self.wait.until(
                EC.element_to_be_clickable(
                    (
                        (
                            By.XPATH,
                            "/html/body/div[1]/div[4]/div[2]/div/div/div/div[1]/div[6]",
                        )
                    )
                )
            )

            # find input tag
            start_button = start_buttons.find_elements_by_tag_name("input")[0]
            start_button.click()
            logging.info("Started roulette")
        except NoSuchElementException as e:
            logging.error("Couldn't find start button")
            raise e
        except TimeoutException as e:
            logging.error("Couldn't find the div containg the start button")
            raise e

    def quit(self):
        """Stops the bot"""
        self.driver.quit()
