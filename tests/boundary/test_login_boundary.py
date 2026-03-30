import pytest
import allure
from pages.login_page import LoginPage
from utils.data_generator import TestDataGenerator

@pytest.mark.boundary
@pytest.mark.login
@allure.epic("Boundary Testing")
@allure.feature("Login Functionality")
class TestLoginBoundary:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.login_page = LoginPage(page)
        self.data_gen = TestDataGenerator()
        self.login_page.navigate("/login")

    @allure.story("Username Boundary Testing")
    @allure.title("Test login with empty username")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_username(self):
        """Test scenario with empty username"""
        self.login_page.login("", "valid_password")
        self.login_page.verify_error_message("Please enter username")

    @allure.story("Username Boundary Testing")
    @allure.title("Test login with very long username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_very_long_username(self):
        """Test with extremely long username (boundary value)"""
        long_username = "a" * 256  # Exceeds database field limit
        self.login_page.login(long_username, "valid_password")
        self.login_page.verify_error_message("Username too long")

    @allure.story("Password Boundary Testing")
    @allure.title("Test login with empty password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_password(self):
        """Test scenario with empty password"""
        self.login_page.login("valid_user", "")
        self.login_page.verify_error_message("Please enter password")

    @allure.story("Password Boundary Testing")
    @allure.title("Test login with minimum length password")
    @allure.severity(allure.severity_level.NORMAL)
    def test_minimum_length_password(self):
        """Test with minimum length password (boundary value)"""
        min_password = "a" * 6  # Assuming minimum length is 6
        self.login_page.login("valid_user", min_password)
        # Should be able to submit successfully

    @allure.story("SQL Injection Testing")
    @allure.title("Test SQL injection attack")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_sql_injection(self):
        """Test SQL injection attack"""
        sql_injection = "' OR '1'='1"
        self.login_page.login(sql_injection, sql_injection)
        # Should display generic error message, not database error
        self.login_page.verify_error_message("Invalid username or password")

    @allure.story("XSS Attack Testing")
    @allure.title("Test XSS script injection")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_xss_injection(self):
        """Test XSS script injection"""
        xss_payload = "<script>alert('xss')</script>"
        self.login_page.login(xss_payload, xss_payload)
        # Input should be escaped or filtered

    @allure.story("Special Characters Testing")
    @allure.title("Test username with special characters")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("special_char", [
        "user@name",
        "user#name",
        "user$name",
        "user%name",
        "user&name",
        "user*name",
        "user(name)",
        "user=name",
        "user+name",
        "user[name]"
    ])
    def test_special_characters_in_username(self, special_char):
        """Test username containing special characters"""
        self.login_page.login(special_char, "valid_password")
        # Validate based on business rules

    @allure.story("Performance Boundary Testing")
    @allure.title("Test rapid successive logins")
    @allure.severity(allure.severity_level.NORMAL)
    def test_rapid_successive_logins(self):
        """Test rapid successive logins (prevent brute force attacks)"""
        for i in range(10):
            self.login_page.login("test_user", "wrong_password")

        # After 10 attempts, CAPTCHA or account lock should appear
        self.login_page.verify_element_present(".captcha-container")

    @allure.story("Internationalization Boundary Testing")
    @allure.title("Test username with Unicode characters")
    @allure.severity(allure.severity_level.NORMAL)
    def test_unicode_username(self):
        """Test username with Unicode characters"""
        unicode_username = "用户名字🎯测试"
        self.login_page.login(unicode_username, "valid_password")
        # Verify proper handling

    @allure.story("Whitespace Handling Testing")
    @allure.title("Test username with leading/trailing spaces")
    @allure.severity(allure.severity_level.NORMAL)
    def test_username_with_spaces(self):
        """Test if leading/trailing spaces are trimmed from username"""
        self.login_page.login("  testuser  ", "valid_password")
        # Verify based on requirements

    @allure.story("Case Sensitivity Testing")
    @allure.title("Test username case sensitivity")
    @allure.severity(allure.severity_level.NORMAL)
    def test_username_case_sensitivity(self):
        """Test whether username is case sensitive"""
        self.login_page.login("TestUser", "valid_password")
        # Verify based on business requirements