# XYZ Bank — Automation Framework

A data-driven automation framework for the [Globals QA Banking Project](https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login) built with **Python**, **Playwright**, and **pytest**.

---

## Architecture & Design

This framework is built with a focus on **robustness**, **maintainability**, and **ease of debugging**.

### Page Object Model (POM) with Wrapper
Every view is represented by a class in the `pages/` directory.
- **BasePage wrapper**: All pages inherit from `base_page.py`. This adds an abstraction layer that ensures consistency and isolates tests from changes in the Playwright API.
- **TestBase inheritance**: All test classes inherit from `TestBase`, which automatically handles fixture injection (`self.page`), keeping the test code clean and focused.

### Data-Driven Strategy
- **External Configuration**: Environment settings like `URL`, `Browser`, and `Timeout` are managed via `config.json`.
- **External Test Data**: All test data (customer names, search queries, etc.) is externalized in `testdata/testdata.json`. The framework uses a dedicated utility (`read_data.py`) to pull this data dynamically.

### Enhanced Reliability & Debugging
- **Screenshot on Failure**: The framework automatically captures a screenshot the moment a test fails and saves it to `report/screenshots/`.
- **Self-Contained Reports**: Generates a detailed, standalone HTML report (`report/report.html`) after every test run.

---

## Project Structure

```bash
Nordhealth-test/
├── config.json                 # Global configuration (URL, Browser, etc.)
├── conftest.py                 # Pytest hooks, screenshot logic, & fixtures
├── pyproject.toml              # Pytest & tooling config
├── testcases.md                # Detailed plain-text test case descriptions
├── environments/
│   └── envs.json               # Environment-specific URLs
├── testdata/
│   └── testdata.json           # External JSON test data reservoir
├── pages/
│   ├── base_page.py            # Playwright action wrapper
│   ├── login_page.py           # Login flows
│   ├── account_page.py         # Customer dashboard interactions
│   ├── deposit_page.py         # Deposit form interactions
│   ├── withdrawal_page.py       # Withdrawal form interactions
│   ├── transactions_page.py    # Transaction list interactions
│   └── manager_page.py         # Bank Manager dashboard
├── tests/
│   ├── test_base.py            # Base test class for setup/teardown
│   ├── test_customer_e2e_flow.py # Login/Logout verification
│   ├── test_account_operations.py # Financial transaction testing
│   └── test_manager_operations.py # Administrative workflow testing
├── utils/
│   ├── read_config.py          # Configuration parser
│   ├── read_data.py            # Test data parser
│   ├── assertions.py           # Reusable assertion helpers
│   └── logger.py               # Logging utility
└── report/
    ├── report.html             # Automated test execution report
    └── screenshots/            # Failure screenshots (generated on failure)
```

---

## Setup & Execution

### 1. Prerequisites
- Python 3.10+
- Virtual Environment (recommended)

### 2. Installation
```bash
pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Run All Tests
```bash
pytest -v
```

### 4. Headed Execution (See the UI)
```bash
pytest --headed -v
```

---

## Framework Summary

| Module | Features |
|---|---|
| **Reporting** | HTML reports and timestamped failure screenshots. |
| **Data-Driven** | Parametrized tests using external JSON and automated teardown. |
| **Cross-Browser** | Configuration-based switching between Chromium, Firefox, and WebKit via `config.json`. |
| **Clean Code** | Clean code principles, POM and modular inheritance patterns has been followed. |
