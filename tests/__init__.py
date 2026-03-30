"""
Test Module

This is the main test module containing all test suites for the Playwright
test automation framework. The module is organized into subdirectories based
on test type and purpose.
"""

# Import test modules for easier access
from tests.api import (
    TestAuthAPI,
    TestProductsAPI,
    TestOrdersAPI,
    TestAPIPerformance
)

from tests.boundary import (
    TestLoginBoundary
)

from tests.performance import (
    PerformanceTestBase,
    PerformanceMetrics,
    TestPageLoadPerformance,
    TestActionPerformance,
    TestAPIPerformance as PerformanceAPITests,
    TestLoadTesting,
    PerformanceMonitor,
    LoadTestSimulator
)

from tests.regression import (
    TestFullWorkflow
)

from tests.smoke import (
    TestSmokeTests
)

__all__ = [
    # API Tests
    "TestAuthAPI",
    "TestProductsAPI",
    "TestOrdersAPI",
    "TestAPIPerformance",
    
    # Boundary Tests
    "TestLoginBoundary",
    
    # Performance Tests
    "PerformanceTestBase",
    "PerformanceMetrics",
    "TestPageLoadPerformance",
    "TestActionPerformance",
    "TestLoadTesting",
    "PerformanceMonitor",
    "LoadTestSimulator",
    
    # Regression Tests
    "TestFullWorkflow",
    
    # Smoke Tests
    "TestSmokeTests",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
Test Module
===========

This module serves as the main entry point for all test suites in the
Playwright test automation framework.

Module Structure:
----------------

tests/
├── __init__.py          # Main test module initialization
├── conftest.py          # Pytest fixtures and hooks
├── api/                 # API test cases
│   ├── test_auth_api.py        # Authentication tests
│   ├── test_products_api.py    # Product API tests
│   ├── test_orders_api.py      # Order API tests
│   └── test_performance_api.py # API performance tests
│
├── boundary/            # Boundary and edge case tests
│   └── test_login_boundary.py  # Login form boundary tests
│
├── performance/         # Performance test cases
│   ├── performance_base.py          # Base classes and metrics
│   ├── test_page_load_performance.py # Page load tests
│   ├── test_action_performance.py   # Action performance tests
│   ├── test_api_performance.py      # API performance tests
│   └── test_load_test.py            # Load and stress tests
│
├── regression/          # Regression test cases
│   └── test_full_workflow.py        # Complete workflow tests
│
└── smoke/               # Smoke test cases
    └── test_smoke.py                # Critical path tests

Test Categories:
---------------

1. Smoke Tests (@pytest.mark.smoke)
   - Fast, critical path tests
   - Run on every commit
   - Verify basic functionality

2. Regression Tests (@pytest.mark.regression)
   - Comprehensive workflow tests
   - Run before releases
   - Ensure no breaking changes

3. API Tests (@pytest.mark.api)
   - REST API endpoint validation
   - Authentication and authorization
   - Data validation

4. Performance Tests (@pytest.mark.performance)
   - Page load performance
   - API response times
   - Load and stress testing

5. Boundary Tests (@pytest.mark.boundary)
   - Edge cases
   - Security testing
   - Input validation

Usage Examples:
--------------

1. Import test classes in your test files:
    from tests import TestSmokeTests, TestFullWorkflow
    
    class MyCustomTests(TestSmokeTests):
        # Inherit all smoke test functionality
        pass

2. Run specific test categories:
    # Run all smoke tests
    pytest -m smoke
    
    # Run all API tests
    pytest -m api
    
    # Run performance tests
    pytest -m performance

3. Run tests with specific markers:
    pytest -m "smoke or regression"
    pytest -m "api and not performance"

4. Run tests in specific directories:
    pytest tests/smoke/
    pytest tests/api/test_auth_api.py

5. Use fixtures in tests:
    def test_example(page, config, api_client):
        # Use built-in fixtures
        pass

Common Fixtures Available:
-------------------------

- page: Playwright page object
- context: Browser context
- config: Environment configuration
- api_client: API client for HTTP requests
- authenticated_api_client: API client with auth token
- test_data: Generated test data
- browser_context_args: Browser context arguments

Configuration:
------------

Test configuration is managed through:
- pytest.ini: Pytest settings and markers
- config/config.yaml: Environment and test configuration
- config/test_data.yaml: Test data
- .env: Environment variables

Best Practices:
--------------

1. Test Organization:
   - Place tests in appropriate subdirectories
   - Use descriptive test names
   - Add docstrings to test functions

2. Test Markers:
   - Always add appropriate markers (@pytest.mark.*)
   - Use markers to categorize and filter tests

3. Test Data:
   - Use fixtures for test data
   - Generate dynamic data with TestDataGenerator
   - Avoid hardcoding values

4. Assertions:
   - Use descriptive assertion messages
   - Validate both positive and negative scenarios
   - Check status codes, response data, and side effects

5. Test Independence:
   - Each test should be independent
   - Clean up after tests
   - Use fresh data for each test

6. Performance:
   - Keep smoke tests fast (< 5 min total)
   - Use parallel execution for large suites
   - Mark slow tests with @pytest.mark.slow

For more details, refer to the individual test files and documentation
in each subdirectory.
"""

# Test markers reference
# These markers can be used to categorize and filter tests:

MARKERS_REFERENCE = """
Test Markers Reference:
----------------------
- @pytest.mark.smoke      : Critical path tests
- @pytest.mark.regression : Full regression tests
- @pytest.mark.boundary   : Edge case and boundary tests
- @pytest.mark.performance: Performance and load tests
- @pytest.mark.api        : API endpoint tests
- @pytest.mark.ui         : UI automation tests
- @pytest.mark.slow       : Long-running tests
- @pytest.mark.security   : Security-related tests
- @pytest.mark.integration: Integration tests
- @pytest.mark.health     : System health checks

Usage Examples:
--------------
@pytest.mark.smoke
def test_critical_function():
    pass

@pytest.mark.api
@pytest.mark.regression
def test_api_endpoint():
    pass
"""

# Helper function to get all test modules
def get_test_modules():
    """
    Get a list of all available test modules in the tests directory.
    
    Returns:
        dict: Dictionary of test categories and their modules
    """
    return {
        "api": [
            "test_auth_api",
            "test_products_api", 
            "test_orders_api",
            "test_performance_api"
        ],
        "boundary": [
            "test_login_boundary"
        ],
        "performance": [
            "test_page_load_performance",
            "test_action_performance",
            "test_api_performance",
            "test_load_test"
        ],
        "regression": [
            "test_full_workflow"
        ],
        "smoke": [
            "test_smoke"
        ]
    }

# Helper function to get test markers
def get_markers():
    """
    Get a list of all available pytest markers.
    
    Returns:
        dict: Dictionary of markers and their descriptions
    """
    return {
        "smoke": "Critical path tests",
        "regression": "Full regression tests",
        "boundary": "Edge case and boundary tests",
        "performance": "Performance and load tests",
        "api": "API endpoint tests",
        "ui": "UI automation tests",
        "slow": "Long-running tests",
        "security": "Security-related tests",
        "integration": "Integration tests",
        "health": "System health checks"
    }

# Module initialization logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Test module initialized")