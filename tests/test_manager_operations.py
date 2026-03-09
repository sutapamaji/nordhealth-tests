import pytest
from pages.manager_page import ManagerPage
from tests.test_base import TestBase
from utils.read_data import get_test_data
from utils.assertions import Assertions

NEW_CUST = get_test_data("new_customer", {})
DEL_CUST = get_test_data("customer_to_delete", {})
SEARCH_Q = get_test_data("search_query", "Harry")

class TestManagerOperations(TestBase):
    """Tests for the Bank Manager workflows."""

    def test_add_customer(self):
        """Verify that a manager can successfully add a new customer and see them in the list."""
        manager = ManagerPage.navigate_to_manager(self.page)

        alert_text = manager.add_customer(NEW_CUST["first_name"], NEW_CUST["last_name"], NEW_CUST["post_code"])
        
        Assertions.assert_contains_text(alert_text, "Customer added successfully", f"Expected success alert, got: '{alert_text}'")

        names = manager.get_customer_names()
        Assertions.assert_contains_text(names, NEW_CUST["first_name"], f"Expected '{NEW_CUST['first_name']}' in customer list, got: {names}")

    def test_delete_customer(self):
        """Verify that a manager can delete an existing customer from the list."""
        manager = ManagerPage.navigate_to_manager(self.page)

        manager.add_customer(DEL_CUST["first_name"], DEL_CUST["last_name"], DEL_CUST["post_code"])

        names_before = manager.get_customer_names()
        Assertions.assert_contains_text(names_before, DEL_CUST["first_name"], f"Setup failed: '{DEL_CUST['first_name']}' not found after adding, got: {names_before}")

        manager.delete_customer(DEL_CUST["first_name"])

        names_after = manager.get_customer_names()
        Assertions.assert_not_contains_text(names_after, DEL_CUST["first_name"], f"Expected '{DEL_CUST['first_name']}' to be removed, but still in list: {names_after}")

    def test_search_customer(self):
        """Verify that a manager can search and filter the customer list."""
        manager = ManagerPage.navigate_to_manager(self.page)

        manager.search_customer(SEARCH_Q)

        rows = self.page.locator("table tbody tr").all()
        visible_names = []
        for row in rows:
            cells = row.locator("td").all()
            if cells:
                visible_names.append(cells[0].text_content() or "")

        Assertions.assert_condition(len(visible_names) >= 1, f"Expected at least one result when searching for '{SEARCH_Q}', got: {visible_names}")
        Assertions.assert_condition(all(SEARCH_Q in name for name in visible_names), f"Expected all visible names to contain '{SEARCH_Q}', got: {visible_names}")

    def test_add_customer_empty_first_and_last_name_validation(self):
        """Verify validation when first name and last name are empty on Add Customer form."""
        manager = ManagerPage.navigate_to_manager(self.page)

        manager.go_to_add_customer()
        manager.do_click(manager._ADD_CUSTOMER_SUBMIT)

        first_name_validation = manager.get_validation_message(manager._FIRST_NAME)
        Assertions.assert_contains_text(
            first_name_validation,
            "Please fill in this field",
            f"Expected 'Please fill in this field' validation for empty first name, got: '{first_name_validation}'",
        )

    def test_open_account_empty_fields_validation(self):
        """Verify validation when customer and currency are empty on Open Account form."""
        manager = ManagerPage.navigate_to_manager(self.page)

        manager.go_to_open_account()
        manager.do_click(manager._PROCESS_BTN)

        customer_validation = manager.get_validation_message(manager._CUSTOMER_SELECT)
        Assertions.assert_contains_text(customer_validation, "Please select", f"Expected 'Please select' validation for empty customer selection, got: '{customer_validation}'")
