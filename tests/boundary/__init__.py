"""
Boundary Test Module

This module contains boundary and edge case test scenarios for validating
system behavior at extreme limits including:
- Empty values and null inputs
- Maximum and minimum length inputs
- Special characters and Unicode
- SQL injection and XSS attacks
- Numeric boundaries (max, min, zero, negative)
- Date and time boundaries
- File size and type boundaries
- Concurrent request boundaries
"""

__all__ = [
    "TestLoginBoundary",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
Boundary Testing Module
=======================

This module provides comprehensive boundary and edge case testing capabilities:

Available Test Classes:
----------------------

- TestLoginBoundary: Login form boundary tests including:
  - Empty username/password
  - Very long username/password
  - SQL injection attacks
  - XSS attacks
  - Special characters
  - Unicode characters
  - Rapid successive logins
  - Case sensitivity tests

Test Categories:
---------------

1. Input Validation:
   - Empty strings and null values
   - Maximum length strings
   - Minimum length strings
   - Special characters (@#$%^&*)
   - Unicode characters (emojis, multi-byte)
   - Whitespace handling (leading/trailing spaces)

2. Security Boundaries:
   - SQL injection payloads
   - XSS (Cross-Site Scripting) attacks
   - Command injection attempts
   - Path traversal attacks

3. Numeric Boundaries:
   - Zero values
   - Negative numbers
   - Maximum integer limits
   - Decimal precision

4. Concurrency Boundaries:
   - Rapid successive requests
   - Rate limiting
   - Race conditions

Usage Examples:
--------------

1. Basic boundary test:
    @pytest.mark.boundary
    def test_empty_username(self):
        self.login_page.login("", "valid_password")
        self.login_page.verify_error_message("Username cannot be empty")

2. Length boundary test:
    @pytest.mark.boundary
    def test_very_long_username(self):
        long_username = "a" * 256
        self.login_page.login(long_username, "valid_password")
        self.login_page.verify_error_message("Username too long")

3. SQL injection test:
    @pytest.mark.boundary
    def test_sql_injection(self):
        sql_injection = "' OR '1'='1"
        self.login_page.login(sql_injection, sql_injection)
        self.login_page.verify_error_message("Invalid credentials")

For more details, refer to test_login_boundary.py in this directory.
"""

# Boundary test markers
# These markers are used in pytest.ini:
# - boundary: All boundary and edge case tests
# - security: Security-related boundary tests

# Test data can be found in:
# - config/test_data.yaml: Contains boundary test cases
# - utils/data_generator.py: Generates boundary test data dynamically