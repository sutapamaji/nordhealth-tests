from playwright.sync_api import Page
from pages.base_page import BasePage
from pages.transactions_page import TransactionsPage
from pages.deposit_page import DepositPage
from pages.withdrawal_page import WithdrawalPage

class AccountPage(BasePage):
    """Encapsulates the customer account dashboard interactions."""

    _WELCOME_TEXT = "span.fontBig"
    _BALANCE_FIELDS = "div.center strong.ng-binding"
    _TRANSACTIONS_TAB = "button[ng-click=\"transactions()\"]"
    _DEPOSIT_TAB = "button[ng-click=\"deposit()\"]"
    _WITHDRAWAL_TAB = "button[ng-click=\"withdrawl()\"]"
    _LOGOUT_BTN = "button.logout"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_welcome_text(self) -> str:
        """Return the welcome banner text."""
        return self.get_text(self._WELCOME_TEXT)

    def get_balance(self) -> int:
        """Return the current account balance."""
        self.page.locator(self._BALANCE_FIELDS).first.wait_for(state="visible", timeout=5000)
        elements = self.page.locator(self._BALANCE_FIELDS).all()
        balance_text = elements[1].text_content() or "0"
        return int(balance_text)

    def get_account_number(self) -> str:
        """Return the displayed account number."""
        self.page.locator(self._BALANCE_FIELDS).first.wait_for(state="visible", timeout=5000)
        elements = self.page.locator(self._BALANCE_FIELDS).all()
        return (elements[0].text_content() or "").strip()

    def go_to_transactions(self) -> TransactionsPage:
        """Click Transactions tab and return TransactionsPage."""
        self.do_click(self._TRANSACTIONS_TAB)
        self.page.wait_for_url("**/listTx", timeout=10000)
        result = TransactionsPage(self.page)
        return result

    def go_to_deposit(self) -> DepositPage:
        """Click Deposit tab and return DepositPage."""
        self.do_click(self._DEPOSIT_TAB)
        self.page.wait_for_selector("label:has-text('Amount to be Deposited :')", timeout=10000)
        return DepositPage(self.page)

    def go_to_withdrawal(self) -> WithdrawalPage:
        """Click Withdrawal tab and return WithdrawalPage."""
        self.do_click(self._WITHDRAWAL_TAB)
        self.page.wait_for_selector("label:has-text('Amount to be Withdrawn :')", timeout=10000)
        return WithdrawalPage(self.page)

    def logout(self):
        """Click Logout button."""
        self.do_click(self._LOGOUT_BTN)
