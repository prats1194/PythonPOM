"""
Base Page Class
Parent class for all page objects
"""

import logging
from playwright.sync_api import Page, expect
from utilities.common_methods import CommonMethods


class BasePage:
    """Base class for all page objects"""

    def __init__(self, page: Page):
        self.page = page
        self.common = CommonMethods(page)
        self.logger = logging.getLogger(self.__class__.__name__)

    def wait_for_page_ready(self):
        """Wait for page to be fully loaded"""
        self.common.wait_for_page_load()

    def get_page_title(self) -> str:
        """Get current page title"""
        return self.page.title()

    def get_current_url(self) -> str:
        """Get current URL"""
        return self.page.url

    def take_screenshot(self, name: str = None):
        """Take screenshot of current page"""
        return self.common.take_screenshot(name)

    def verify_page_loaded(self, expected_url_part: str = None, expected_title: str = None):
        """Verify page is loaded correctly"""
        if expected_url_part:
            self.common.verify_url_contains(expected_url_part)
        if expected_title:
            self.common.verify_title(expected_title)
        self.logger.info("Page loaded successfully")