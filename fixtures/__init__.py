"""
Pytest fixtures module for test setup and teardown
"""
from fixtures.browser_fixture import (
    playwright_instance,
    browser,
    browser_context_args,
    browser_context
)
from fixtures.data_fixture import (
    test_data_generator,
    user_data,
    product_data,
    boundary_test_cases,
    test_config_data,
    browser_type,
    api_test_data
)

__all__ = [
    "playwright_instance",
    "browser",
    "browser_context_args",
    "browser_context",
    "test_data_generator",
    "user_data",
    "product_data",
    "boundary_test_cases",
    "test_config_data",
    "browser_type",
    "api_test_data"
]