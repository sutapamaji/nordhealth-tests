from playwright.sync_api import Page
from utils.logger import get_logger

class BasePage:
    """Wrapper class containing common interactions for Playwright."""
    
    def __init__(self, page: Page):
        self.page = page
        self.log = get_logger(self.__class__.__name__)

    def do_click(self, selector: str):
        self.log.info(f"Clicking on element: {selector}")
        self.page.wait_for_selector(selector, state="visible")
        self.page.click(selector)

    def do_fill(self, selector: str, text: str):
        self.log.info(f"Filling element '{selector}' with text: {text}")
        self.page.wait_for_selector(selector, state="visible")
        self.page.fill(selector, text)

    def get_text(self, selector: str) -> str:
        text = self.page.text_content(selector) or ""
        self.log.info(f"Retrieved text from '{selector}': {text}")
        return text

    def is_visible(self, selector: str) -> bool:
        visible = self.page.is_visible(selector)
        self.log.info(f"Element '{selector}' visibility: {visible}")
        return visible