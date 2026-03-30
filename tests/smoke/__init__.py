"""
Smoke Test Module

This module contains critical path smoke tests that verify the most important
functionality of the application. Smoke tests are designed to be:
- Fast to execute
- Cover core functionality
- Run on every commit/deployment
- Provide quick feedback on system health
"""

__all__ = [
    "TestSmokeTests",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
Smoke Testing Module
===================

This module provides critical path smoke tests that validate core application
functionality:

Available Test Classes:
----------------------

- TestSmokeTests: Critical path smoke tests
  - Login functionality
  - Dashboard access
  - Product search
  - Add to cart
  - Checkout process
  - Order confirmation

Smoke Test Characteristics:
--------------------------

1. Speed: Smoke tests should complete in under 5 minutes
2. Coverage: Test only the most critical user journeys
3. Reliability: Tests should be highly stable with minimal flakiness
4. Frequency: Run on every code commit and deployment

Test Categories:
---------------

1. Authentication:
   - Valid login
   - Invalid login
   - Logout functionality

2. Core Features:
   - Dashboard access
   - Product listing
   - Search functionality

3. Key Transactions:
   - Add to cart
   - Checkout
   - Order placement

4. System Health:
   - Page load
   - API availability
   - Database connectivity

Usage Examples:
--------------

1. Basic smoke test:
    from tests.smoke import TestSmokeTests
    
    def test_valid_login(self):
        self.login_page.navigate("/login")
        self.login_page.login(config.username, config.password)
        self.dashboard_page.verify_login_success()

2. Critical path smoke test:
    def test_critical_user_journey(self):
        # Login
        self.login_page.login(config.username, config.password)
        
        # Search and add to cart
        self.dashboard_page.search_product("test")
        self.product_page.add_to_cart()
        
        # Checkout
        self.cart_page.proceed_to_checkout()
        
        # Verify order placement
        self.cart_page.verify_checkout_page()

3. API health smoke test:
    def test_api_health(self, api_client):
        response = api_client.get("/health")
        assert response["status_code"] == 200
        assert response["data"]["status"] == "healthy"

Smoke Test Execution Strategy:
----------------------------

1. Pre-commit: Run smoke tests before merging code
2. Post-deployment: Run smoke tests after deployment
3. Production monitoring: Run smoke tests periodically in production
4. Alerting: Configure alerts for smoke test failures

For more details, refer to test_smoke.py in this directory.
"""

# Smoke test markers
# These markers are used in pytest.ini:
# - smoke: Critical path smoke tests
# - health: System health checks

# Smoke test configuration can be found in:
# - config/config.yaml: Environment configurations
# - config/test_data.yaml: Test data for smoke tests