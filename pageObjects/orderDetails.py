"""
Order Details Page Object
"""

from playwright.sync_api import expect
from utilities.common_methods import CommonMethods

class OrderDetailsPage(CommonMethods):
    """Order details page actions and elements"""

    # Locators
    TAGLINE_MESSAGE = ".tagline"

    # Expected Messages
    SUCCESS_MESSAGE = "Thank you for Shopping With Us"

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def verifyOrderMessage(self):
        """Verify order success message is displayed"""
        #expect(self.page.locator(self.TAGLINE_MESSAGE)).to_contain_text(self.SUCCESS_MESSAGE)
        self.verify_text_present(self.TAGLINE_MESSAGE, self.SUCCESS_MESSAGE)