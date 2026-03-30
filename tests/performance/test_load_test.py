"""
Load and Stress Tests
"""
import pytest
import allure
from tests.performance.performance_base import PerformanceTestBase
from utils.performance_monitor import LoadTestSimulator, PerformanceMonitor
from pages.product_page import ProductPage
import time


@pytest.mark.performance
@pytest.mark.slow
@allure.epic("Performance Testing")
@allure.feature("Load Testing")
class TestLoadTesting:
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.page = page
        self.config = config
        self.performance_test = PerformanceTestBase(page)
        self.load_simulator = LoadTestSimulator()
        self.monitor = PerformanceMonitor()
    
    @allure.story("Concurrent Users")
    @allure.title("Test concurrent user load on product page")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_concurrent_product_page_load(self):
        """Test loading product page with concurrent users"""
        
        def load_product_page():
            # Create new page for each user
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(f"{self.config.base_url}/product/1")
                page.wait_for_load_state("networkidle")
                browser.close()
        
        # Simulate 50 concurrent users
        result = self.load_simulator.simulate_concurrent_users(50, load_product_page)
        
        # Assert performance metrics
        assert result["avg"] < 5000, f"Average response time {result['avg']}ms exceeded 5000ms"
        assert result["p95"] < 8000, f"95th percentile {result['p95']}ms exceeded 8000ms"
        assert result["success_count"] == 50, f"Only {result['success_count']}/50 requests succeeded"
        
        # Attach report to Allure
        report = self.load_simulator.generate_load_test_report()
        allure.attach(report, name="Load Test Report", 
                     attachment_type=allure.attachment_type.MARKDOWN)
    
    @allure.story("Concurrent Users")
    @allure.title("Test concurrent API requests")
    @allure.severity(allure.severity_level.NORMAL)
    def test_concurrent_api_requests(self, api_client):
        """Test concurrent API request performance"""
        
        def make_api_call():
            return api_client.get("/products")
        
        # Test with increasing load
        load_levels = [10, 25, 50, 100]
        results = []
        
        for load in load_levels:
            result = self.load_simulator.simulate_concurrent_users(load, make_api_call)
            results.append(result)
            
            # Log results
            allure.attach(
                f"Concurrent Users: {load}\n"
                f"Average Response: {result['avg']:.2f}ms\n"
                f"95th Percentile: {result['p95']:.2f}ms\n"
                f"Success Rate: {result['success_count']}/{load}",
                name=f"Load Test - {load} Users",
                attachment_type=allure.attachment_type.TEXT
            )
        
        # Verify performance degradation is acceptable
        avg_increase = results[-1]["avg"] / results[0]["avg"]
        assert avg_increase < 5, f"Performance degradation too high: {avg_increase}x"
    
    @allure.story("Stress Testing")
    @allure.title("Test system under high load")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_stress_test_api(self, api_client):
        """Stress test API with sustained high load"""
        
        def make_api_call():
            return api_client.get("/products")
        
        # Simulate sustained load for 30 seconds
        self.monitor.start_session("API Stress Test")
        
        import threading
        import time
        
        stop_flag = threading.Event()
        
        def sustained_load():
            while not stop_flag.is_set():
                start_time = time.time()
                response = make_api_call()
                response_time = (time.time() - start_time) * 1000
                self.monitor.record_metric("API Response Time", response_time)
                time.sleep(0.1)  # 10 requests per second
        
        # Run load for 30 seconds
        load_thread = threading.Thread(target=sustained_load)
        load_thread.start()
        
        time.sleep(30)
        stop_flag.set()
        load_thread.join()
        
        # End session and generate report
        session_data = self.monitor.end_session()
        report = self.monitor.generate_report()
        
        allure.attach(report, name="Stress Test Report", 
                     attachment_type=allure.attachment_type.MARKDOWN)
        
        # Verify system stability
        assert session_data["statistics"]["p99"] < 10000, "99th percentile exceeded 10 seconds"
        assert session_data["statistics"]["avg"] < 2000, "Average response time exceeded 2 seconds"