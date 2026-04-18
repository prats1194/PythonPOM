"""
Dashboard Page Object
"""

from .ordersHistory import OrdersHistoryPage
from utilities.common_methods import CommonMethods  # ← ADD THIS IMPORT


class DashboardPage(CommonMethods):
    """Dashboard page actions and elements"""

    # Locators
    ORDERS_BUTTON = " ORDERS"

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def selectOrdersNavLink(self):
        """Click on Orders navigation link"""
        self.click_by_role("button", self.ORDERS_BUTTON)  # ← Using common method
        self.wait_for_page_load()  # ← Optional: wait for page to load
        orderHistoryPage = OrdersHistoryPage(self.page)
        return orderHistoryPage