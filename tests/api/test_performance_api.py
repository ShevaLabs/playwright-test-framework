"""
API Performance Tests
"""
import pytest
import allure
import time
from utils.api_client import APIClient

@allure.epic("API Testing")
@allure.feature("API Performance")
class TestAPIPerformance:
    
    @allure.story("Response Time")
    @allure.title("Test API response time for endpoints")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("endpoint", [
        "/products",
        "/categories",
        "/health",
        "/api/version"
    ])
    def test_response_time(self, api_client, endpoint, config):
        """Test API response time within threshold"""
        threshold = config.get_test_config().get("api_response_threshold", 2000)
        
        start_time = time.time()
        response = api_client.get(endpoint)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        assert response["status_code"] == 200
        assert response_time < threshold, f"Response time {response_time}ms exceeded threshold {threshold}ms"
        
        # Add performance data to Allure
        allure.attach(
            f"Response Time: {response_time:.2f}ms\nThreshold: {threshold}ms",
            name="Performance Metrics",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.story("Concurrent Requests")
    @allure.title("Test concurrent API requests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_concurrent_requests(self, api_client):
        """Test handling of concurrent API requests"""
        import concurrent.futures
        
        def make_request():
            return api_client.get("/products")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [f.result() for f in futures]
        
        # Check all requests succeeded
        successful = sum(1 for r in results if r["status_code"] == 200)
        assert successful == len(results), f"Only {successful}/{len(results)} requests succeeded"
        
        allure.attach(
            f"Total requests: {len(results)}\nSuccessful: {successful}",
            name="Concurrent Test Results",
            attachment_type=allure.attachment_type.TEXT
        )