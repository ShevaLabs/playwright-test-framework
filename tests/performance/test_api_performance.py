"""
API Performance Tests
"""
import pytest
import allure
import time
import statistics
from utils.performance_monitor import PerformanceMonitor


@pytest.mark.performance
@pytest.mark.api
@allure.epic("Performance Testing")
@allure.feature("API Performance")
class TestAPIPerformance:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.monitor = PerformanceMonitor()
    
    @allure.story("Response Time")
    @allure.title("Test API endpoint response times")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("endpoint", [
        "/products",
        "/categories",
        "/health",
        "/api/version"
    ])
    def test_api_response_time(self, api_client, endpoint, config):
        """Test response time for various API endpoints"""
        thresholds = config.get_test_config().get("api_response_threshold", 2000)
        
        response_times = []
        
        # Make multiple requests to get average
        for i in range(5):
            start_time = time.time()
            response = api_client.get(endpoint)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            response_times.append(response_time)
            
            assert response["status_code"] == 200
        
        avg_response_time = statistics.mean(response_times)
        
        # Attach metrics
        metrics_text = f"""
        ### API Performance Metrics - {endpoint}
        
        - **Average Response Time**: {avg_response_time:.2f} ms
        - **Min Response Time**: {min(response_times):.2f} ms
        - **Max Response Time**: {max(response_times):.2f} ms
        - **Median Response Time**: {statistics.median(response_times):.2f} ms
        - **Standard Deviation**: {statistics.stdev(response_times) if len(response_times) > 1 else 0:.2f} ms
        - **Threshold**: {thresholds} ms
        """
        
        allure.attach(metrics_text, name=f"Performance Metrics - {endpoint}",
                     attachment_type=allure.attachment_type.MARKDOWN)
        
        assert avg_response_time < thresholds, \
            f"Average response time {avg_response_time}ms exceeded threshold {thresholds}ms"
    
    @allure.story("Response Time")
    @allure.title("Test authenticated endpoint performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_authenticated_endpoint_performance(self, authenticated_api_client):
        """Test performance of authenticated endpoints"""
        endpoints = ["/user/profile", "/orders", "/wishlist"]
        
        for endpoint in endpoints:
            response_times = []
            
            for i in range(3):
                start_time = time.time()
                response = authenticated_api_client.get(endpoint)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                response_times.append(response_time)
                
                if response["status_code"] != 200:
                    allure.attach(
                        f"Endpoint: {endpoint}\nStatus: {response['status_code']}",
                        name="Non-200 Response",
                        attachment_type=allure.attachment_type.TEXT
                    )
            
            avg_time = statistics.mean(response_times)
            assert avg_time < 3000, f"Endpoint {endpoint} avg response time {avg_time}ms exceeded 3000ms"
    
    @allure.story("Database Query Performance")
    @allure.title("Test database query performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_database_query_performance(self, api_client):
        """Test performance of database-intensive endpoints"""
        
        # Test pagination performance
        page_sizes = [10, 25, 50, 100]
        
        for size in page_sizes:
            start_time = time.time()
            response = api_client.get(f"/products?limit={size}")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            
            allure.attach(
                f"Page Size: {size}\nResponse Time: {response_time:.2f}ms",
                name=f"Pagination Performance - {size} items",
                attachment_type=allure.attachment_type.TEXT
            )
            
            assert response_time < 2000, f"Query with {size} items took {response_time}ms"
    
    @allure.story("Search Performance")
    @allure.title("Test search endpoint performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("search_term", [
        "a",  # Single character
        "test",  # Common term
        "very long search term with many words",  # Long query
        "nonexistentproductxyz123",  # No results
    ])
    def test_search_performance(self, api_client, search_term):
        """Test search endpoint performance with various queries"""
        start_time = time.time()
        response = api_client.get("/products/search", params={"q": search_term})
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        
        assert response["status_code"] == 200
        assert response_time < 1500, f"Search for '{search_term}' took {response_time}ms"
        
        allure.attach(
            f"Search Term: {search_term}\n"
            f"Response Time: {response_time:.2f}ms\n"
            f"Results Count: {len(response['data'])}",
            name=f"Search Performance - {search_term}",
            attachment_type=allure.attachment_type.TEXT
        )