"""
Regression Test Module

This module contains comprehensive regression test suites for validating
that existing functionality continues to work after changes. Regression tests
cover all critical user journeys and business workflows including:
- End-to-end user journeys
- Cross-functional workflows
- Integration scenarios
- Data persistence validation
- System integration tests
- Critical path validations
"""

__all__ = [
    "TestFullWorkflow",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
Regression Testing Module
=========================

This module provides comprehensive regression testing capabilities to ensure
application stability and prevent regression bugs:

Available Test Classes:
----------------------

- TestFullWorkflow: Complete business workflow regression tests
  - Complete shopping flow (login → search → add to cart → checkout → order)
  - Shopping cart boundary cases
  - Inventory concurrency tests
  - Page load performance tests
  - Cross-browser compatibility tests

Test Categories:
---------------

1. End-to-End Workflows:
   - Complete shopping flow
   - User registration flow
   - Account management flow
   - Order history and tracking

2. Cross-Functional Integration:
   - UI to API integration
   - Database consistency checks
   - Cache invalidation validation
   - Third-party service integration

3. Data Integrity Tests:
   - Data creation, update, deletion
   - Data validation rules
   - Database constraints
   - Data synchronization

4. Multi-User Scenarios:
   - Concurrent user operations
   - Data isolation between users
   - Permission and role-based access

5. Cross-Browser Compatibility:
   - Chrome/Chromium
   - Firefox
   - WebKit/Safari
   - Edge

Usage Examples:
--------------

1. Complete workflow regression test:
    from tests.regression import TestFullWorkflow
    
    def test_complete_shopping_flow(self, test_data):
        # Login
        self.login_page.login(config.username, config.password)
        
        # Search and add to cart
        self.dashboard_page.search_product(test_data["product_name"])
        self.product_page.add_to_cart()
        
        # Checkout
        self.cart_page.proceed_to_checkout()
        self.cart_page.fill_shipping_info(test_data["shipping_info"])
        
        # Place order
        order_id = self.cart_page.place_order()
        assert order_id is not None

2. Cross-browser regression test:
    @pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
    def test_cross_browser_compatibility(self, browser_type):
        # Test critical flows across all browsers
        pass

3. Data integrity regression test:
    def test_inventory_concurrency(self, browser_context):
        # Test concurrent inventory updates
        pass

Regression Test Execution Strategy:
---------------------------------

1. Full Regression: Run all regression tests before major releases
2. Smoke Regression: Run critical path tests on every commit
3. Selective Regression: Run tests related to changed components
4. Nightly Regression: Complete regression suite runs overnight

For more details, refer to test_full_workflow.py in this directory.
"""

# Regression test markers
# These markers are used in pytest.ini:
# - regression: Full regression test suite
# - smoke: Critical path regression tests
# - slow: Long-running regression tests
# - integration: Integration regression tests

# Test data can be found in:
# - config/test_data.yaml: Comprehensive test data sets
# - fixtures/data_fixture.py: Test data fixtures