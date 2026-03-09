# Test Cases

This document details the automated test cases covered by the framework for the Globals QA Banking Project.

## 1. Customer Operations (test_customer_e2e_flow.py)

**TC-01: Verify successful login and logout for a valid customer**
- The user is on the banking application's login landing page.
- The user is navigated to the customer account dashboard, and a welcome message containing the customer's name should be displayed.
- Verify deposit, withdrawal and transaction tabs are visible.
- The user should be logged out successfully.

---

## 2. Customer Account Operations (test_account_operations.py)

*Note: All account operations use Harry Potter as the test customer.*

**TC-02: Verify deposit positive flow**
- **Steps**: Login -> Deposit 500 -> Verify Balance -> Check Transactions.
- **Expected Result**: "Deposit Successful" message appears. Balance increases by 500. A new entry appears in the transaction history.

**TC-03: Verify empty deposit amount shows validation and no transaction**
- **Steps**: Login -> Navigate to Deposit -> Click Submit without entering an amount.
- **Expected Result**: Browser validation message contains "Please fill in this field". Transaction table unchanged.

**TC-04: Verify negative deposit amount is ignored**
- **Steps**: Login -> Navigate to Deposit -> Enter -100 and Click Submit.
- **Expected Result**: Balance remains unchanged. No success message is displayed.

**TC-05: Verify withdrawal positive flow**
- **Steps**: Login -> Deposit 200 -> Withdraw 100 -> Verify Balance -> Check Transactions.
- **Expected Result**: "Transaction successful" message appears. Balance reflects the net change. Transaction history shows the operations.

**TC-06: Verify withdrawal more than balance fails**
- **Steps**: Login -> Attempt to withdraw an amount > current balance.
- **Expected Result**: "Transaction Failed" message appears. The account balance remains unchanged.

**TC-07: Verify empty withdrawal amount shows validation and no transaction**
- **Steps**: Login -> Navigate to Withdraw -> Click Submit without entering an amount.
- **Expected Result**: Browser validation message contains "Please fill in this field". Transaction table unchanged.

**TC-08: Verify negative withdrawal amount is ignored**
- **Steps**: Login -> Navigate to Withdraw -> Enter -100 and Click Submit.
- **Expected Result**: Balance remains unchanged. No success message is displayed.

---

## 3. Bank Manager Operations (test_manager_operations.py)

**TC-11: Verify the Bank Manager can add a new customer**
- **Preconditions**: The user is on the Bank Manager dashboard.
- **Expected Result**: An alert dialog confirms: "Customer added successfully". The new customer is present in the table of registered customers.

**TC-12: Verify the Bank Manager can delete an existing customer**
- **Preconditions**: The user is on the Bank Manager dashboard.
- **Expected Result**: The selected customer is successfully removed from the table and is no longer present in the list.

**TC-13: Verify the Bank Manager can search/filter the customer list**
- **Preconditions**: The user is on the Bank Manager dashboard and there are multiple customers in the system.
- **Expected Result**: At least one result is shown matching the search query. All visible rows contain the search term.
