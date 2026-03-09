from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Encapsulates interactions with the login(Customer/Manager) page."""

    _CUSTOMER_LOGIN_BTN = "button:has-text('Customer Login')"
    _MANAGER_LOGIN_BTN = "button:has-text('Bank Manager Login')"
    _USER_SELECT = "#userSelect"
    _LOGIN_BTN = "button[type='submit']"

    def __init__(self, page: Page):
        super().__init__(page)

    def click_customer_login(self):
        """Click the 'Customer Login' button on the home screen."""
        self.do_click(self._CUSTOMER_LOGIN_BTN)

    def click_manager_login(self):
        """Click the 'Bank Manager Login' button on the home screen."""
        self.do_click(self._MANAGER_LOGIN_BTN)

    def select_customer(self, name: str):
        """Select a customer by visible name from the dropdown."""
        self.page.select_option(self._USER_SELECT, label=name)

    def click_login(self):
        """Click the Login submit button."""
        self.do_click(self._LOGIN_BTN)

    def login_as_customer(self, name: str):
        """Full convenience flow: Customer Login → select name → Login."""
        self.click_customer_login()
        self.select_customer(name)
        self.click_login()

    def is_user_select_visible(self) -> bool:
        """Check if the customer selection dropdown is visible."""
        return self.is_visible(self._USER_SELECT)
