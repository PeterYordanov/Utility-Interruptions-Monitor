#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: Email sender - takes in the gathered (scraped) information, composes an email and sends it.
Author: Petar Yordanov
Date: 2025-04-16
"""

from __future__ import print_function
import logging, brevo_python
from brevo_python.rest import ApiException
from html_email_builder import HTMLEmailBuilder


class EmailSender:
    """
    A class to send HTML emails using Brevo (Sendinblue) transactional email API.

    Attributes:
        api_instance: The Brevo TransactionalEmailsApi instance.
        sender_email: The email sender object used in SMTP emails.
        sender_name: Display name of the sender.
    """

    def __init__(
        self, api_key: str, sender_email: str, sender_name: str = "Notifier"
    ) -> None:
        """
        Initializes the EmailSender with the API key and sender information.

        Args:
            api_key (str): Brevo API key.
            sender_email (str): Sender's email address.
            sender_name (str): Sender's display name.
        """
        configuration = brevo_python.Configuration()
        configuration.api_key["api-key"] = api_key
        self.api_instance = brevo_python.TransactionalEmailsApi(
            brevo_python.ApiClient(configuration)
        )
        self.sender_email = brevo_python.SendSmtpEmailSender(
            email=sender_email, name=sender_name
        )
        self.sender_name = sender_name

    def send_template_email(
        self, to_emails: list, params: dict, headers: dict = None
    ) -> object:
        """
        Sends a formatted HTML email using predefined interruption data.

        Args:
            to_emails (list): List of recipient email addresses.
            params (dict): Email content parameters (e.g., vik_items, energopro_items).
            headers (dict, optional): Optional email headers.

        Returns:
            object: Response from the Brevo API if successful.

        Raises:
            ApiException: If the API call fails.
        """
        if headers is None:
            headers = {}

        to_formatted = [
            brevo_python.SendSmtpEmailTo(email=email) for email in to_emails
        ]

        logging.debug("Constructing HTML email...")

        builder = HTMLEmailBuilder()
        html_content = builder.build_html(
            vik_items=params.get("vik_items", []),
            energopro_items=params.get("energopro_items", []),
        )

        logging.info("Sending email...")

        email_payload = brevo_python.SendSmtpEmail(
            sender=self.sender_email,
            to=to_formatted,
            html_content=html_content,
            subject="Нови Прекъсвания на Услуги",
        )

        try:
            response = self.api_instance.send_transac_email(email_payload)
            logging.debug(response)
            return response
        except ApiException as e:
            logging.error(
                "Exception when calling TransactionalEmailsApi->send_transac_email: %s\n"
                % e
            )
            raise
