#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description: Brief description of what this file does.
Author: Petar Yordanov
Date: 2025-04-16
"""


class HTMLEmailBuilder:
    """
    Builds an HTML email body from interruption data for ВиК and Енерго Про.
    """

    def build_html(self, vik_items: list, energopro_items: list) -> str:
        """
        Builds a full HTML document from interruption sections.

        Args:
            vik_items (list): List of ВиК interruption items.
            energopro_items (list): List of Енерго Про interruption items.

        Returns:
            str: A complete HTML string for the email body.
        """
        html = ["<!DOCTYPE html>", "<html>", "<body>"]
        html.append(self._build_vik_section(vik_items))
        html.append(self._build_energopro_section(energopro_items))
        html.append(self._build_footer())
        html.append("</body></html>")
        return "".join(html)

    def _build_vik_section(self, vik_items: list) -> str:
        """
        Builds the section for ВиК interruptions.

        Args:
            vik_items (list): ВиК interruptions.

        Returns:
            str: HTML string of the ВиК section.
        """
        html = ["<div><h2>🔵 ВиК - Велико Търново</h2>"]
        if vik_items:
            for item in vik_items:
                html.append(
                    f"""
                    <p><strong>📅 {item.get('date')}</strong><br>
                    📝 {item.get('title')}<br>
                    📄 {item.get('text')}<br>
                    🔗 <a href="{item.get('link')}">Прочети повече</a></p>
                    <hr>
                    """
                )
        else:
            html.append("<p>ℹ️ Няма нови ВиК прекъсвания.</p>")
        html.append("</div>")
        return "".join(html)

    def _build_energopro_section(self, energopro_items: list) -> str:
        """
        Builds the section for Енерго Про interruptions.

        Args:
            energopro_items (list): Енерго Про interruptions.

        Returns:
            str: HTML string of the Енерго Про section.
        """
        html = ["<div><h2>🟠 Енерго Про - Велико Търново</h2>"]
        if energopro_items:
            for item in energopro_items:
                html.append(
                    f"""
                    <p>🕒 {item.get('period')}<br>
                    📄 {item.get('text')}</p>
                    <hr>
                    """
                )
        else:
            html.append("<p>ℹ️ Няма нови електро прекъсвания.</p>")
        html.append("</div>")
        return "".join(html)

    def _build_footer(self) -> str:
        """
        Builds the email footer.

        Returns:
            str: HTML footer string.
        """
        return """
        <footer>
          <p style="font-size: 12px; color: #888;">
            Това е автоматично съобщение. За повече информация посетете официалните сайтове.
          </p>
        </footer>
        """
