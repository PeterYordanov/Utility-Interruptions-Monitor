#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Filename: example.py
Description: EnergoPro scraper that takes in interruptions data for electricity.
Author: Petar Yordanov
Date: 2025-04-16
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging, time
from base_scraper import BaseScraper


class EnergoProInterruptionsScraper(BaseScraper):
    """
    Scraper for energy outage information from Energo Pro Veliko Tarnovo's website.
    Inherits from BaseScraper.
    """

    def __init__(self, url: str) -> None:
        """
        Initializes the scraper with the provided URL.
        """
        super().__init__(url)

    def click_second_marker(self) -> None:
        """
        Clicks on the second marker in the leaflet map to trigger content load.
        """
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "img.leaflet-marker-icon")
                )
            )
            markers = self.driver.find_elements(
                By.CSS_SELECTOR, "img.leaflet-marker-icon"
            )

            if len(markers) >= 2:
                logging.info("Clicking the second map marker.")
                self.driver.execute_script("arguments[0].scrollIntoView();", markers[1])
                self.driver.execute_script("arguments[0].click();", markers[1])
                time.sleep(2)
            else:
                logging.warning("Less than 2 markers found. Exiting.")
                self.driver.quit()
                exit()
        except Exception as e:
            logging.error(f"Error clicking marker: {e}")
            self.driver.quit()
            exit()

    def extract_interruptions(self) -> list[dict]:
        """
        Extracts a list of energy interruptions based on predefined keywords.

        Returns:
            list[dict]: A list of dictionaries with 'period' and 'text' keys.
        """
        interruptions = []

        try:
            self.wait.until(
                lambda d: len(
                    d.find_element(By.ID, "interruption_areas")
                    .get_attribute("innerHTML")
                    .strip()
                )
                > 10
            )
            ul = self.driver.find_element(By.ID, "interruption_areas")
            items = ul.find_elements(By.TAG_NAME, "li")

            logging.info(f"Found {len(items)} interruptions.")

            for i, item in enumerate(items, 1):
                try:
                    period = item.find_element(By.CLASS_NAME, "period").text.strip()
                    text = item.find_element(By.CLASS_NAME, "text").text.strip()

                    logging.info(
                        f"\n--- INTERRUPTION #{i} ---\nPeriod: {period}\nText: {text}"
                    )

                    if "Патреш" in text or ("Павликени" in text and "Руски" in text):
                        interruptions.append({"period": period, "text": text})
                        logging.info("Added the interruption to the list!")

                except Exception as e:
                    logging.warning(f"Error parsing interruption #{i}: {e}")

        except Exception as e:
            logging.error("No interruptions loaded or timeout: %s", e)

        return interruptions

    def run(self) -> list[dict]:
        """
        Orchestrates the scraping process.

        Returns:
            list[dict]: List of interruption entries.
        """
        self.click_second_marker()
        interruptions = self.extract_interruptions()
        self.driver.quit()
        logging.info("Scraping complete. Browser closed.")
        return interruptions
