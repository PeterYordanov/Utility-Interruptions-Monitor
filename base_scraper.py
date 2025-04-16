#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: Base scraper, to be inherited by each scraper.
Author: Petar Yordanov
Date: 2025-04-16
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import logging


class BaseScraper:
    """
    A base class for setting up and managing a headless Chrome browser
    session using Selenium for web scraping.

    Attributes:
        url (str): The target URL to open in the browser.
        driver (webdriver.Chrome): The Selenium Chrome WebDriver instance.
        wait_time (int): The number of seconds to wait for elements to load.
        wait (WebDriverWait): The WebDriverWait object used for waiting.
    """

    def __init__(self, url: str, wait_time: int = 20):
        """
        Initializes the BaseScraper with the given URL and wait time.

        Args:
            url (str): The URL to navigate to.
            wait_time (int, optional): The time to wait for elements. Defaults to 20 seconds.
        """
        self.url = url
        self.driver = None
        self.wait_time = wait_time
        self.wait = None
        self.setup_browser()

    def setup_browser(self) -> None:
        """
        Sets up a headless Chrome browser session using Selenium,
        configures options, and navigates to the target URL.
        """
        logging.info("Setting up headless Chrome browser...")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        logging.info("Setting up Chrome driver...")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.url)
        self.wait = WebDriverWait(self.driver, self.wait_time)

    def quit_browser(self) -> None:
        """
        Closes the browser session and quits the WebDriver instance.
        """
        if self.driver:
            self.driver.quit()
            logging.info("Browser closed.")
