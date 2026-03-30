from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class Modal(BasePage):
    """Modal dialog component"""
    
    # Locators
    MODAL_CONTAINER = ".modal"
    MODAL_TITLE = ".modal-title"
    MODAL_BODY = ".modal-body"
    MODAL_FOOTER = ".modal-footer"
    CLOSE_BUTTON = ".modal-close"
    CONFIRM_BUTTON = ".modal-confirm"
    CANCEL_BUTTON = ".modal-cancel"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Wait for modal to appear")
    def wait_for_modal(self, timeout: int = 5000) -> None:
        """Wait for modal to become visible"""
        self.wait_for_element(self.MODAL_CONTAINER, timeout)
    
    @allure.step("Get modal title")
    def get_title(self) -> str:
        """Get modal title text"""
        return self.get_text(self.MODAL_TITLE)
    
    @allure.step("Get modal body text")
    def get_body_text(self) -> str:
        """Get modal body text content"""
        return self.get_text(self.MODAL_BODY)
    
    @allure.step("Confirm modal action")
    def confirm(self) -> None:
        """Click confirm button"""
        self.click(self.CONFIRM_BUTTON)
    
    @allure.step("Cancel modal action")
    def cancel(self) -> None:
        """Click cancel button"""
        self.click(self.CANCEL_BUTTON)
    
    @allure.step("Close modal")
    def close(self) -> None:
        """Close modal using close button"""
        self.click(self.CLOSE_BUTTON)
    
    @allure.step("Verify modal is closed")
    def verify_closed(self) -> None:
        """Verify modal is no longer visible"""
        self.wait_for_element(self.MODAL_CONTAINER, timeout=1000)
        # Element should not be visible
    
    @allure.step("Verify modal content: {expected_text}")
    def verify_content(self, expected_text: str) -> None:
        """Verify modal contains expected text"""
        body_text = self.get_body_text()
        assert expected_text in body_text, f"Expected '{expected_text}' in modal body, got '{body_text}'"
    
    @allure.step("Press escape key to close")
    def press_escape(self) -> None:
        """Press ESC key to close modal"""
        self.page.keyboard.press("Escape")