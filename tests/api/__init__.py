"""
API Test Module

This module contains API test cases for validating RESTful API endpoints including:
- Authentication (login, register, logout)
- CRUD operations (create, read, update, delete)
- Data validation and schema validation
- Error handling and edge cases
- API security testing
- API performance testing
"""

__all__ = [
    "TestAuthAPI",
    "TestProductsAPI",
    "TestOrdersAPI",
    "TestAPIPerformance",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
API Testing Module
==================

This module provides comprehensive API testing capabilities including:

- RESTful API Testing: GET, POST, PUT, DELETE operations
- Authentication: Bearer token, Basic Auth, OAuth2 support
- Request/Response Validation: Status codes, headers, body content
- Schema Validation: JSON schema validation for responses
- Data-Driven Testing: Parameterized tests with various data sets
- Error Handling: Testing error scenarios and edge cases
- Security Testing: SQL injection, XSS, authentication bypass
- Performance Testing: Response time monitoring and load testing

Available Test Classes:
----------------------

- TestAuthAPI: Authentication and authorization tests
- TestProductsAPI: Product CRUD operations and search tests
- TestOrdersAPI: Order management and processing tests
- TestAPIPerformance: API response time and load tests

Usage Examples:
--------------

1. Using API test classes:
    from tests.api import TestProductsAPI
    
    class TestMyAPI(TestProductsAPI):
        def test_custom_endpoint(self):
            # Inherit all product API tests
            pass

2. Using fixtures in API tests:
    def test_get_products(api_client):
        response = api_client.get("/products")
        assert response["status_code"] == 200

3. Parameterized API tests:
    @pytest.mark.parametrize("endpoint", ["/products", "/categories"])
    def test_api_endpoints(api_client, endpoint):
        response = api_client.get(endpoint)
        assert response["status_code"] == 200

For more details, refer to the individual test files in this directory:
- test_auth_api.py: Authentication and authorization tests
- test_products_api.py: Product CRUD operations
- test_orders_api.py: Order management tests
- test_performance_api.py: API performance and load tests
"""

# API test markers
# These markers are used in pytest.ini:
# - api: All API tests
# - smoke: Critical API tests
# - regression: Full API regression tests
# - performance: API performance tests
# - security: API security tests

# API test data can be found in:
# - config/test_data.yaml: Test data configurations
# - config/config.yaml: Environment configurations