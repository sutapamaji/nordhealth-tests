import pytest
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from tests.test_base import TestBase
from utils.read_data import get_test_data
from utils.assertions import Assertions

CUSTOMERS = get_test_data("customers", [])

class TestCustomerE2EFlow(TestBase):
    """Tests for the Customer Login/Logout E2E flow."""

    @pytest.mark.parametrize(
        "customer_name",
        CUSTOMERS,
        ids=[c.replace(" ", "_").lower() for c in CUSTOMERS] if CUSTOMERS else None,
    )
    def test_customer_login_logout_e2e(self, customer_name):
        """Verify the complete E2E flow: login, navigation to all tabs and logout."""
        login = LoginPage(self.page)
        account = AccountPage(self.page)

        login.login_as_customer(customer_name)
        
        welcome_text = account.get_welcome_text()
        Assertions.assert_contains_text(welcome_text, customer_name, f"Expected '{customer_name}' in welcome text, but got: '{welcome_text}'")

        transactions = account.go_to_transactions()
        Assertions.assert_condition(transactions.is_visible(), "Failed to land on Transactions page")
        transactions.click_back()

        deposit = account.go_to_deposit()
        Assertions.assert_condition(deposit.is_visible(), "Failed to land on Deposit page")

        withdrawal = account.go_to_withdrawal()
        Assertions.assert_condition(withdrawal.is_visible(), "Failed to land on Withdrawal page")

        account.logout()

        Assertions.assert_condition(login.is_user_select_visible(), f"Expected user selection dropdown to be visible after {customer_name} logout")
