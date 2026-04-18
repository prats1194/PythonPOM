"""
Test POM Code - End to End Test Suite
"""

import sys
import json
import pytest
from pathlib import Path
from playwright.sync_api import Playwright

# Project root path configuration
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Page Object imports
from pageObjects.login import LoginPage

# Test Data Configuration
TEST_DATA_PATH = project_root / 'Testdata' / 'credentials.json'

with open(TEST_DATA_PATH) as f:
    test_data = json.load(f)

user_credentials_list = test_data['user_credentials']

# Test Data Constants
ORDER_ID = "69dbf40cf86ba51a655ee478"


@pytest.mark.sanity
@pytest.mark.parametrize('user_credentials', user_credentials_list)
def test_e2e01(playwright: Playwright, browserInstance, user_credentials):
    """End-to-end test: Login -> Navigate to Orders -> Verify Order Details"""

    # Extract credentials
    userName = user_credentials["userEmail"]
    password = user_credentials["password"]

    # Login Page
    loginPage = LoginPage(browserInstance)
    loginPage.navigate()
    dashboardPage = loginPage.login(userName, password)

    # Dashboard Page -> Orders History
    orderHistoryPage = dashboardPage.selectOrdersNavLink()

    # Orders History -> Order Details
    orderDetailsPage = orderHistoryPage.selectOrder(ORDER_ID)

    # Verify Order Message
    orderDetailsPage.verifyOrderMessage()