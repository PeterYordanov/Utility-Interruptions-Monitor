import logging
import json
from energo_pro_interruptions_scraper import EnergoProInterruptionsScraper

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("interruption_scraper.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":

    with open("settings.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    scraper = EnergoProInterruptionsScraper(data["energo_pro_url"])
    interruptions = scraper.run()

    logging.info(interruptions)
