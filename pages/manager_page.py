from playwright.sync_api import Page
from pages.base_page import BasePage


class ManagerPage(BasePage):
    """Encapsulates the Bank Manager dashboard interactions."""

    @staticmethod
    def navigate_to_manager(page: Page):
        """Helper: navigate to the Manager Login and return the ManagerPage."""
        from pages.login_page import LoginPage
        login = LoginPage(page)
        login.click_manager_login()
        return ManagerPage(page)

    _ADD_CUSTOMER_TAB = "button[ng-click=\"addCust()\"]"
    _OPEN_ACCOUNT_TAB = "button[ng-click=\"openAccount()\"]"
    _CUSTOMERS_TAB = "button[ng-click=\"showCust()\"]"

    _FIRST_NAME = "input[placeholder='First Name']"
    _LAST_NAME = "input[placeholder='Last Name']"
    _POST_CODE = "input[placeholder='Post Code']"
    _ADD_CUSTOMER_SUBMIT = "button[type='submit']"

    _CUSTOMER_SELECT = "#userSelect"
    _CURRENCY_SELECT = "#currency"
    _PROCESS_BTN = "button[type='submit']"

    _SEARCH_INPUT = "input[placeholder='Search Customer']"
    _CUSTOMER_ROWS = "table tbody tr"
    _DELETE_BTN = "button[ng-click=\"deleteCust(cust)\"]"

    def __init__(self, page: Page):
        super().__init__(page)

    def get_validation_message(self, selector: str) -> str:
        """Return the validation message for given input/select."""
        return self.page.eval_on_selector(selector, "el => el.validationMessage")

    def go_to_add_customer(self):
        """Switch to the Add Customer tab."""
        self.do_click(self._ADD_CUSTOMER_TAB)

    def go_to_open_account(self):
        """Switch to the Open Account tab."""
        self.do_click(self._OPEN_ACCOUNT_TAB)

    def go_to_customers(self):
        """Switch to the Customers list tab."""
        self.do_click(self._CUSTOMERS_TAB)

    def add_customer(self, first_name: str, last_name: str, post_code: str) -> str:
        """Fill in the Add Customer form and submit it."""
        self.go_to_add_customer()
        self.do_fill(self._FIRST_NAME, first_name)
        self.do_fill(self._LAST_NAME, last_name)
        self.do_fill(self._POST_CODE, post_code)

        alert_message = []

        def _handle_dialog(dialog):
            alert_message.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", _handle_dialog)

        self.do_click(self._ADD_CUSTOMER_SUBMIT)
        self.page.wait_for_timeout(500)

        return alert_message[0] if alert_message else ""

    def open_account(self, customer_name: str, currency: str) -> str:
        """Open a new account for a customer with the given currency."""
        self.go_to_open_account()
        self.page.select_option(self._CUSTOMER_SELECT, label=customer_name)
        self.page.select_option(self._CURRENCY_SELECT, label=currency)

        alert_message = []

        def _handle_dialog(dialog):
            alert_message.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", _handle_dialog)

        self.do_click(self._PROCESS_BTN)
        self.page.wait_for_timeout(500)

        return alert_message[0] if alert_message else ""

    def search_customer(self, query: str):
        """Type into the search box to filter the customer list."""
        self.go_to_customers()
        self.do_fill(self._SEARCH_INPUT, query)

    def get_customer_names(self) -> list[str]:
        """Return a list of first names from the visible customer table."""
        self.go_to_customers()
        self.page.locator(self._CUSTOMER_ROWS).first.wait_for(
            state="visible", timeout=5000
        )
        rows = self.page.locator(self._CUSTOMER_ROWS).all()
        names = []
        for row in rows:
            cells = row.locator("td").all()
            if cells:
                names.append(cells[0].text_content() or "")
        return names

    def delete_customer(self, first_name: str):
        """Delete a customer by matching their first name in the table."""
        self.go_to_customers()
        rows = self.page.locator(self._CUSTOMER_ROWS).all()
        for row in rows:
            cells = row.locator("td").all()
            if cells and (cells[0].text_content() or "").strip() == first_name:
                row.locator(self._DELETE_BTN).click()
                return
        raise ValueError(f"Customer '{first_name}' not found in the table")
