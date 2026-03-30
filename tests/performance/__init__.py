"""
Performance Test Module

This module contains performance test cases for measuring and validating
application performance metrics including:
- Page load times
- API response times
- User action performance
- Load testing
- Stress testing
- Concurrent user simulation
"""

from tests.performance.performance_base import PerformanceTestBase, PerformanceMetrics
from utils.performance_monitor import PerformanceMonitor, LoadTestSimulator

__all__ = [
    # Base classes
    "PerformanceTestBase",
    "PerformanceMetrics",
    
    # Test classes
    "TestPageLoadPerformance",
    "TestActionPerformance",
    "TestAPIPerformance",
    "TestLoadTesting",
    
    # Utilities
    "PerformanceMonitor",
    "LoadTestSimulator",
]

# Module version
__version__ = "1.0.0"

# Module description
__doc__ = """
Performance Testing Module
==========================

This module provides a comprehensive set of tools and test cases for
performance testing, including:

Available Test Classes:
----------------------

1. TestPageLoadPerformance: Page load performance tests
   - Home page load time
   - Login page load time
   - Product listing page load time
   - Search results page load time
   - Cart page load time

2. TestActionPerformance: User action performance tests
   - Login action response time
   - Search action response time
   - Add to cart action response time
   - Checkout action response time
   - Element rendering performance

3. TestAPIPerformance: API endpoint performance tests
   - GET endpoint response times
   - POST endpoint response times
   - Database query performance
   - Search endpoint performance

4. TestLoadTesting: Load and stress tests
   - Concurrent user simulation
   - Load testing with increasing users
   - Stress testing with sustained load
   - System stability under high load

Performance Metrics:
-------------------

- Page Load Time: Total time to load the page
- First Contentful Paint (FCP): Time to first content rendering
- Largest Contentful Paint (LCP): Time to largest content rendering
- DOM Content Loaded: Time to DOM tree construction
- Server Response Time: Time to first byte from server
- Time to Interactive: Time to become fully interactive
- API Response Time: End-to-end API response time
- Throughput: Requests per second

Usage Examples:
--------------

1. Page load performance test:
    from tests.performance import TestPageLoadPerformance
    
    def test_home_page_load(self):
        thresholds = {
            "page_load_time": 3000,
            "first_contentful_paint": 1500
        }
        result = self.performance_test.measure_page_load(self.config.base_url)
        self.performance_test.assert_performance_threshold(thresholds)

2. Action performance test:
    from tests.performance import TestActionPerformance
    
    def test_login_action(self):
        action_time, _ = self.performance_test.measure_action_performance(
            perform_login, "login_action"
        )
        assert action_time < 2000

3. Load test:
    from tests.performance import LoadTestSimulator
    
    simulator = LoadTestSimulator()
    result = simulator.simulate_concurrent_users(50, api_call_function)
    assert result["avg"] < 5000

For more details, refer to the individual test files in this directory:
- performance_base.py: Base classes and metrics collection
- test_page_load_performance.py: Page load performance tests
- test_action_performance.py: Action performance tests
- test_api_performance.py: API performance tests
- test_load_test.py: Load and stress tests
"""

# Performance test markers
# These markers are used in pytest.ini:
# - performance: All performance tests
# - slow: Long-running load and stress tests

# Performance thresholds can be configured in:
# - config/config.yaml: Performance thresholds and baselines