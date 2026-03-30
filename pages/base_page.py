from typing import Optional, Tuple, List, Any
from playwright.sync_api import Page, Locator, expect
from datetime import datetime
import allure
from utils.logger import logger
from utils.screenshot import ScreenshotHelper

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.screenshot = ScreenshotHelper(page)
        self.logger = logger
        self.timeout = 30000

    def navigate(self, url: str) -> None:
        """Navigate to the specified URL"""
        with allure.step(f"Navigate to: {url}"):
            self.logger.info(f"Navigating to: {url}")
            self.page.goto(url)

    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Click on element"""
        with allure.step(f"Click element: {selector}"):
            self.logger.info(f"Clicking element: {selector}")
            self.page.click(selector, timeout=timeout or self.timeout)

    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Fill text in input field"""
        with allure.step(f"Fill {selector} with: {text}"):
            self.logger.info(f"Filling {selector} with: {text}")
            self.page.fill(selector, text, timeout=timeout or self.timeout)

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """Get element text content"""
        return self.page.text_content(selector, timeout=timeout or self.timeout)

    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> Locator:
        """Wait for element to appear"""
        return self.page.locator(selector).first.wait_for(
            state="visible",
            timeout=timeout or self.timeout
        )

    def wait_for_url(self, url_pattern: str, timeout: Optional[int] = None) -> None:
        """Wait for URL to match pattern"""
        self.page.wait_for_url(url_pattern, timeout=timeout or self.timeout)

    def take_screenshot(self, name: Optional[str] = None) -> str:
        """Take screenshot"""
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        return self.screenshot.capture(name)

    def verify_element_present(self, selector: str, timeout: Optional[int] = None) -> None:
        """Verify element is present"""
        with allure.step(f"Verify element exists: {selector}"):
            expect(self.page.locator(selector)).to_be_visible(
                timeout=timeout or self.timeout
            )

    def verify_text_present(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """Verify text is present"""
        with allure.step(f"Verify text exists: {text}"):
            expect(self.page.locator(selector)).to_contain_text(
                text,
                timeout=timeout or self.timeout
            )

    def select_dropdown_option(self, selector: str, option_text: str) -> None:
        """Select dropdown option"""
        with allure.step(f"Select dropdown option: {option_text}"):
            self.page.select_option(selector, label=option_text)

    def hover(self, selector: str) -> None:
        """Hover mouse over element"""
        self.page.hover(selector)

    def switch_to_iframe(self, selector: str) -> None:
        """Switch to iframe"""
        frame = self.page.frame_locator(selector)
        return frame

    def execute_js(self, script: str, *args) -> Any:
        """Execute JavaScript code"""
        return self.page.evaluate(script, *args)

    def clear_input(self, selector: str) -> None:
        """Clear input field"""
        self.page.fill(selector, "")
        self.page.press(selector, "Backspace")

    def get_all_elements(self, selector: str) -> List[Locator]:
        """Get all matching elements"""
        return self.page.locator(selector).all()

    def is_element_enabled(self, selector: str) -> bool:
        """Check if element is enabled"""
        return self.page.locator(selector).is_enabled()

    def is_element_checked(self, selector: str) -> bool:
        """Check if checkbox is checked"""
        return self.page.locator(selector).is_checked()

    def upload_file(self, selector: str, file_path: str) -> None:
        """Upload file"""
        with allure.step(f"Upload file: {file_path}"):
            self.page.set_input_files(selector, file_path)

    def scroll_to_element(self, selector: str) -> None:
        """Scroll to element"""
        self.page.locator(selector).scroll_into_view_if_needed()

    def wait_for_network_idle(self, timeout: Optional[int] = None) -> None:
        """Wait for network to become idle"""
        self.page.wait_for_load_state("networkidle", timeout=timeout or self.timeout)