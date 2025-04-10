from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time

class EnergoProInterruptionsScraper:
    def __init__(self, energo_pro_url: str):
        self.energo_pro_url = energo_pro_url
        self.setup_browser()
        self.wait = WebDriverWait(self.driver, 20)

    def setup_browser(self):
        logging.info("Setting up headless Chrome browser.")
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.energo_pro_url)

    def click_second_marker(self):
        try:
            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.leaflet-marker-icon")))
            markers = self.driver.find_elements(By.CSS_SELECTOR, "img.leaflet-marker-icon")

            if len(markers) >= 2:
                logging.info("Clicking the second map marker.")
                self.driver.execute_script("arguments[0].scrollIntoView();", markers[1])
                self.driver.execute_script("arguments[0].click();", markers[1])
                time.sleep(2)
                self.driver.save_screenshot("after_click.png")
            else:
                logging.warning("Less than 2 markers found. Exiting.")
                self.driver.quit()
                exit()
        except Exception as e:
            logging.error(f"Error clicking marker: {e}")
            self.driver.quit()
            exit()

    def extract_interruptions(self):
        interruptions = []

        try:
            self.wait.until(lambda d: len(d.find_element(By.ID, "interruption_areas").get_attribute("innerHTML").strip()) > 10)
            ul = self.driver.find_element(By.ID, "interruption_areas")
            items = ul.find_elements(By.TAG_NAME, "li")

            logging.info(f"Found {len(items)} interruptions.")

            for i, item in enumerate(items, 1):
                try:
                    period = item.find_element(By.CLASS_NAME, "period").text.strip()
                    text = item.find_element(By.CLASS_NAME, "text").text.strip()

                    logging.info(f"\n--- INTERRUPTION #{i} ---\nPeriod: {period}\nText: {text}")

                    if "Патреш":
                        interruptions.append({
                            period: period,
                            text: text
                        })
                        logging.info("Added the interruption to the list!")

                    if "Павликени" in text and "Руски" in text:
                        interruptions.append({
                            period: period,
                            text: text
                        })
                        logging.info("Added the interruption to the list!")
                except Exception as e:
                    logging.warning(f"Error parsing interruption #{i}: {e}")
        except Exception as e:
            logging.error("No interruptions loaded or timeout: %s", e)
            self.driver.save_screenshot("no_interruption_result.png")

        return interruptions

    def run(self):
        self.click_second_marker()
        interruptions = self.extract_interruptions()
        self.driver.quit()
        logging.info("Scraping complete. Browser closed.")
        return interruptions
