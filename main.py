#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: Run both scrapers, combine their results, send an email.
Author: Petar Yordanov
Date: 2025-04-16
"""

import logging, json
from email_sender import EmailSender
from energo_pro_interruptions_scraper import EnergoProInterruptionsScraper
from vik_vt_interruptions_scraper import VikVtInterruptionsScraper

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler("interruption_scraper.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

if __name__ == "__main__":

    with open("settings.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    vik_vt_scraper = VikVtInterruptionsScraper(data["vik_vt_url"])
    energo_pro_scraper = EnergoProInterruptionsScraper(data["energo_pro_url"])

    vik_vt_interruptions = vik_vt_scraper.run()
    energo_pro_interruptions = energo_pro_scraper.run()

    logging.info(vik_vt_interruptions)
    logging.info(energo_pro_interruptions)

    sender = EmailSender(
        api_key=data["email_token"],
        sender_email=data["email_sender"],
        sender_name="Interruptions Alerts",
    )

    if not vik_vt_interruptions and not energo_pro_interruptions:
        logging.info("No interruptions found. Skipping email.")
    else:
        interruptions_data = {
            "vik_items": vik_vt_interruptions,
            "energopro_items": energo_pro_interruptions,
        }

        sender.send_template_email(
            to_emails=data["email_recipients"],
            params=interruptions_data,
        )
