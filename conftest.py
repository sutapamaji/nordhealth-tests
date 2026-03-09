import pytest
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
from utils.read_config import get_config_value

@pytest.fixture(scope="function")
def app_page(request):
    """
    Initializes Playwright browser and page based on config.json values.
    Provides the active page object to the test.
    """
    playwright = sync_playwright().start()
    
    browser_name = get_config_value("Browser", "chromium")
    headless_mode = get_config_value("Headless", True)
    timeout = get_config_value("Timeout", 5000)
    
    if browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless_mode)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headless_mode)
    else:
        browser = playwright.chromium.launch(headless=headless_mode)
        
    context = browser.new_context(viewport={"width": 1920, "height": 1080})
    page = context.new_page()
    page.set_default_timeout(timeout)
    
    base_url = get_config_value("URL")
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    
    request.node.page = page
    if request.cls:
        request.cls.page = page

    yield page
    
    context.close()
    browser.close()
    playwright.stop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest hook to capture screenshot on test failure.
    Saves automatically to a reports/screenshots folder.
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        page = getattr(item, "page", None)
        if page:
            try:
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                report_dir = os.path.join(os.path.dirname(__file__), "report", "screenshots")
                os.makedirs(report_dir, exist_ok=True)
                screenshot_path = os.path.join(report_dir, f"{item.name}_{timestamp}.png")
                page.screenshot(path=screenshot_path)
            except Exception as e:
                print(f"Failed to take screenshot: {e}")
