"""
Login Page Object
"""
from .dashboard import DashboardPage
from utilities.common_methods import CommonMethods

class LoginPage(CommonMethods):
    """Login page actions and elements"""

    # Locators (CSS selectors for enter_text method)
    EMAIL_INPUT = "input[id='userEmail']"           # ← CSS selector
    PASSWORD_INPUT = "input[id='userPassword']"     # ← CSS selector
    LOGIN_BUTTON = "Login"

    # URLs
    BASE_URL = "https://rahulshettyacademy.com/client"

    def __init__(self, page):
        super().__init__(page)  # Initialize CommonMethods (logger, page)
        self.page = page

    def navigate(self):
        """Navigate to login page"""
        self.navigate_to(self.BASE_URL)
        self.wait_for_page_load()

    def login(self, userEmail, userPassword):
        """Login with provided credentials"""
        self.enter_text(self.EMAIL_INPUT, userEmail)
        self.enter_text(self.PASSWORD_INPUT, userPassword)
        self.click_by_role("button", self.LOGIN_BUTTON)
        dashboardPage = DashboardPage(self.page)
        return dashboardPage