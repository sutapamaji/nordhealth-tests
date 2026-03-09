from pages.login_page import LoginPage
from pages.account_page import AccountPage
from tests.test_base import TestBase
from utils.assertions import Assertions

CUSTOMER = "Harry Potter"

class _AccountOpsBase(TestBase):
    """Shared helpers for account operation tests."""

    def _login(self) -> AccountPage:
        """Helper to log in and return the AccountPage."""
        login = LoginPage(self.page)
        login.login_as_customer(CUSTOMER)
        return AccountPage(self.page)


class TestDeposit(_AccountOpsBase):
    """Deposit-related account operation tests."""

    def test_deposit_positive_flow(self):
        """Verify after successful deposit transaction table should be updated correctly"""
        account = self._login()

        deposit_page = account.go_to_deposit()
        message = deposit_page.deposit_amount(500)
        Assertions.assert_contains_text(message, "Deposit Successful", "Expected 'Deposit Successful' message")

        self.page.wait_for_timeout(1000)

        transactions = account.go_to_transactions()
        count = transactions.get_transaction_count()
        Assertions.assert_condition(count > 0, "No transactions found after deposit")

    def test_deposit_empty_amount_shows_validation_message(self):
        """Verify empty deposit shows validation message and doesn't change transaction state."""
        account = self._login()

        transactions = account.go_to_transactions()
        initial_txn_count = transactions.get_transaction_count()
        transactions.click_back()

        deposit_page = account.go_to_deposit()
        deposit_page.do_click(deposit_page._SUBMIT_BTN)
        val_msg = deposit_page.get_validation_message()
        transactions = account.go_to_transactions()

        Assertions.assert_contains_text(val_msg, "Please fill in this field", f"Expected 'Please fill in this field' validation, got: '{val_msg}'")
        Assertions.assert_equal(transactions.get_transaction_count(), initial_txn_count, "Transaction table should not update on empty deposit submit")

    def test_deposit_negative_amount(self):
        """Verify that a negative deposit amount should not make successful deposit."""
        account = self._login()
        initial_balance = account.get_balance()

        deposit_page = account.go_to_deposit()
        deposit_page.deposit_amount(-100)
        
        Assertions.assert_equal(account.get_balance(), initial_balance, "Balance should not change with negative deposit")


class TestWithdrawal(_AccountOpsBase):
    """Withdrawal-related account operation tests."""

    def test_withdrawal_positive_flow(self):
        """Verify after successful withdrawal transaction table should be updated correctly"""
        account = self._login()

        deposit_page = account.go_to_deposit()
        deposit_page.deposit_amount(200)

        withdrawal_page = account.go_to_withdrawal()
        message = withdrawal_page.withdraw_amount(100)
        Assertions.assert_contains_text(message, "Transaction successful", "Expected 'Transaction successful' message")

        self.page.wait_for_timeout(1000)

        transactions = account.go_to_transactions()
        count = transactions.get_transaction_count()
        Assertions.assert_condition(count > 0, "No transactions found after withdrawal")

    def test_withdrawal_more_than_balance_fails(self):
        """Verify that attempting to withdraw more than the available balance fails."""
        account = self._login()
        initial_balance = account.get_balance()

        withdrawal_page = account.go_to_withdrawal()
        message = withdrawal_page.withdraw_amount(initial_balance + 2000)  # Ensure it exceeds

        Assertions.assert_contains_text(
            message,
            "Transaction Failed",
            f"Expected 'Transaction Failed' in message, got: '{message}'",
        )
        Assertions.assert_equal(account.get_balance(), initial_balance, f"Expected balance to remain {initial_balance}")

    def test_withdraw_empty_amount_shows_validation_message(self):
        """Verify empty withdrawal shows validation message and doesn't change transaction state."""
        account = self._login()

        transactions = account.go_to_transactions()
        initial_txn_count = transactions.get_transaction_count()
        transactions.click_back()

        withdrawal_page = account.go_to_withdrawal()
        withdrawal_page.do_click(withdrawal_page._SUBMIT_BTN)
        val_msg = withdrawal_page.get_validation_message()
        transactions = account.go_to_transactions()

        Assertions.assert_contains_text(val_msg, "Please fill in this field", f"Expected 'Please fill in this field' validation, got: '{val_msg}'")
        Assertions.assert_equal(transactions.get_transaction_count(), initial_txn_count, "Transaction table should not update on empty withdrawal submit")

    def test_withdrawal_negative_amount(self):
        """Verify that a negative withdrawal amount should not make successful withdrawal."""
        account = self._login()
        initial_balance = account.get_balance()

        withdrawal_page = account.go_to_withdrawal()
        withdrawal_page.withdraw_amount(-100)
        
        Assertions.assert_equal(account.get_balance(), initial_balance, "Balance should not change with negative withdrawal")
