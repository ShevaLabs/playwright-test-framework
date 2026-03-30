from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#loginBtn"
    ERROR_MESSAGE = ".error-message"
    REMEMBER_ME_CHECKBOX = "#rememberMe"
    FORGOT_PASSWORD_LINK = "a[href*='forgot-password']"
    SIGNUP_LINK = "a[href*='signup']"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Login operation")
    def login(self, username: str, password: str, remember_me: bool = False) -> None:
        """Perform login operation"""
        self.logger.info(f"Logging in with username: {username}")

        # Boundary test: empty username
        if not username:
            self.logger.warning("Username is empty")

        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)

        if remember_me:
            self.click(self.REMEMBER_ME_CHECKBOX)

        self.click(self.LOGIN_BUTTON)

    @allure.step("Verify error message")
    def verify_error_message(self, expected_message: str) -> None:
        """Verify login error message"""
        actual_message = self.get_text(self.ERROR_MESSAGE)
        assert expected_message in actual_message, \
            f"Expected error message '{expected_message}' not found. Actual: '{actual_message}'"

    @allure.step("Click forgot password")
    def click_forgot_password(self) -> None:
        """Click forgot password link"""
        self.click(self.FORGOT_PASSWORD_LINK)

    @allure.step("Click signup link")
    def click_signup(self) -> None:
        """Click signup link"""
        self.click(self.SIGNUP_LINK)

    @allure.step("Verify login form exists")
    def verify_login_form_present(self) -> None:
        """Verify login form elements exist"""
        self.verify_element_present(self.USERNAME_INPUT)
        self.verify_element_present(self.PASSWORD_INPUT)
        self.verify_element_present(self.LOGIN_BUTTON)

    @allure.step("Test password visibility toggle")
    def test_password_visibility_toggle(self) -> None:
        """Test password show/hide functionality"""
        password_input = self.page.locator(self.PASSWORD_INPUT)

        # Default should be password type
        assert password_input.get_attribute("type") == "password"

        # Click show password button
        show_password_btn = self.page.locator(".show-password-btn")
        show_password_btn.click()

        # Now should be text type
        assert password_input.get_attribute("type") == "text"

        # Click again should revert to password type
        show_password_btn.click()
        assert password_input.get_attribute("type") == "password"