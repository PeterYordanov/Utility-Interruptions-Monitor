#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: VikVt scraper that takes in interruptions data for the water utility.
Author: Petar Yordanov
Date: 2025-04-16
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging
from base_scraper import BaseScraper


class VikVtInterruptionsScraper(BaseScraper):
    """
    Scraper for water service interruptions (ВиК Велико Търново).
    """

    def __init__(self, url: str) -> None:
        """
        Initializes the scraper with the provided URL.
        """
        super().__init__(url)

    def extract_interruptions(self) -> list[dict]:
        """
        Extracts interruption entries containing relevant keywords.

        Returns:
            list[dict]: A list of dictionaries with date, title, text, and link.
        """
        news_items = []

        try:
            self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "list_item"))
            )
            list_items = self.driver.find_elements(By.CLASS_NAME, "list_item")

            logging.info(f"Found {len(list_items)} news items.")

            for i, item in enumerate(list_items, 1):
                try:
                    date = item.find_element(By.CLASS_NAME, "date").text.strip()

                    title_element = item.find_element(By.CLASS_NAME, "text_06")
                    title = title_element.text.strip()

                    link = title_element.find_element(By.TAG_NAME, "a").get_attribute(
                        "href"
                    )

                    text = item.find_element(By.CLASS_NAME, "mb5").text.strip()

                    logging.info(f"News #{i}: {date} - {title}")

                    if any(
                        keyword in title for keyword in ["Павликени", "Патреш"]
                    ) or any(keyword in text for keyword in ["Павликени", "Патреш"]):
                        news_items.append(
                            {"date": date, "title": title, "text": text, "link": link}
                        )
                except Exception as e:
                    logging.warning(f"Error parsing news item #{i}: {e}")
        except Exception as e:
            logging.error("Failed to load or parse news items: %s", e)

        return news_items

    def run(self) -> list[dict]:
        """
        Orchestrates the scraping process.

        Returns:
            list[dict]: List of relevant news items.
        """
        results = self.extract_interruptions()
        self.driver.quit()
        logging.info("Scraping complete. Browser closed.")
        return results
