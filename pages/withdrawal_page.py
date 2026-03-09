from playwright.sync_api import Page
from pages.base_page import BasePage

class WithdrawalPage(BasePage):
    """Encapsulates the Withdrawal view interactions."""

    _AMOUNT_INPUT = "input[placeholder='amount']"
    _SUBMIT_BTN = "button[type='submit']"
    _MESSAGE = "span[ng-show='message']"
    _WITHDRAWAL_LABEL = "label:has-text('Amount to be Withdrawn :')"

    def __init__(self, page: Page):
        super().__init__(page)

    def withdraw_amount(self, amount: int) -> str:
        """Perform a withdrawal and return the resulting message."""
        self.page.locator(self._MESSAGE).wait_for(state="hidden", timeout=3000)
        self.do_fill(self._AMOUNT_INPUT, str(amount))
        self.do_click(self._SUBMIT_BTN)
        return self.get_message()

    def get_message(self) -> str:
        """Return the success/error message."""
        return self.get_text(self._MESSAGE)

    def get_validation_message(self) -> str:
        """Return the HTML5 validation message of the amount input."""
        return self.page.eval_on_selector(self._AMOUNT_INPUT, "el => el.validationMessage")

    def is_visible(self) -> bool:
        """Check if Withdrawal view is visible."""
        self.page.wait_for_selector(self._WITHDRAWAL_LABEL, state="visible", timeout=5000)
        return self.page.is_visible(self._WITHDRAWAL_LABEL)
