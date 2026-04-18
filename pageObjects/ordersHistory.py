"""
Orders History Page Object
"""

from .orderDetails import OrderDetailsPage
from utilities.common_methods import CommonMethods

class OrdersHistoryPage(CommonMethods):
    """Orders history page actions and elements"""

    # Locators
    ORDER_ROW = "tr"
    VIEW_BUTTON = "View"

    def __init__(self, page):
        super().__init__(page)
        self.page = page

    def selectOrder(self, orderId):
        """Select an order by order ID and view details"""
        row = self.page.locator(self.ORDER_ROW).filter(has_text=orderId)
        row.get_by_role("button", name=self.VIEW_BUTTON).click()
        orderDetailsPage = OrderDetailsPage(self.page)
        return orderDetailsPage