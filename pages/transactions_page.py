from playwright.sync_api import Page
from pages.base_page import BasePage
import time

class TransactionsPage(BasePage):
    """Encapsulates the Transactions view interactions."""

    _BACK_BTN = "button[ng-click=\"back()\"]"
    _RESET_BTN = "button[ng-click=\"reset()\"]"
    _TRANSACTION_ROWS = "table tbody tr"

    def __init__(self, page: Page):
        super().__init__(page)

    def click_back(self):
        """Return from Transactions to the main account view."""
        self.do_click(self._BACK_BTN)

    def get_transaction_count(self, timeout_ms: int = 2000) -> int:
        """Return the number of rows in the transaction table."""
        locator = self.page.locator(self._TRANSACTION_ROWS)

        if timeout_ms <= 0:
            return locator.count()

        deadline = time.time() + (timeout_ms / 1000.0)
        while time.time() < deadline:
            count = locator.count()
            if count > 0:
                return count
            self.page.wait_for_timeout(200)

        return locator.count()

    def is_visible(self) -> bool:
        """Check if Transactions view is visible (by checking the Back button)."""
        self.page.wait_for_selector(self._BACK_BTN, state="visible", timeout=5000)
        return self.page.is_visible(self._BACK_BTN)
