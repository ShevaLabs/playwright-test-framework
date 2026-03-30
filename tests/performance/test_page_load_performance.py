"""
Page Load Performance Tests
"""
import pytest
import allure
from tests.performance.performance_base import PerformanceTestBase
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.performance
@allure.epic("Performance Testing")
@allure.feature("Page Load Performance")
class TestPageLoadPerformance:
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.page = page
        self.config = config
        self.performance_test = PerformanceTestBase(page)
    
    @allure.story("Home Page")
    @allure.title("Test home page load performance")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_home_page_load(self):
        """Test home page load performance metrics"""
        thresholds = {
            "page_load_time": 3000,  # 3 seconds
            "first_contentful_paint": 1500,  # 1.5 seconds
            "largest_contentful_paint": 2500,  # 2.5 seconds
            "server_response_time": 500  # 0.5 seconds
        }
        
        result = self.performance_test.measure_page_load(self.config.base_url)
        
        # Assert performance thresholds
        self.performance_test.assert_performance_threshold(thresholds)
        
        # Collect resource load times
        resources = self.performance_test.collect_resource_load_times()
        
        # Verify critical resources loaded quickly
        critical_resources = [r for r in resources if "js" in r["name"] or "css" in r["name"]]
        for resource in critical_resources:
            assert resource["duration"] < 1000, f"Critical resource {resource['name']} took {resource['duration']}ms"
    
    @allure.story("Login Page")
    @allure.title("Test login page load performance")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_page_load(self):
        """Test login page load performance"""
        thresholds = {
            "page_load_time": 2000,
            "first_contentful_paint": 1000,
            "server_response_time": 300
        }
        
        result = self.performance_test.measure_page_load(f"{self.config.base_url}/login")
        self.performance_test.assert_performance_threshold(thresholds)
    
    @allure.story("Product Page")
    @allure.title("Test product listing page performance")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("category", ["electronics", "clothing", "books"])
    def test_product_listing_performance(self, category):
        """Test product listing page load with different categories"""
        thresholds = {
            "page_load_time": 3500,
            "first_contentful_paint": 2000
        }
        
        result = self.performance_test.measure_page_load(
            f"{self.config.base_url}/products?category={category}"
        )
        self.performance_test.assert_performance_threshold(thresholds)
    
    @allure.story("Search Page")
    @allure.title("Test search results page performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_results_performance(self):
        """Test search results page performance"""
        thresholds = {
            "page_load_time": 2500,
            "first_contentful_paint": 1500
        }
        
        result = self.performance_test.measure_page_load(
            f"{self.config.base_url}/search?q=test"
        )
        self.performance_test.assert_performance_threshold(thresholds)
    
    @allure.story("Cart Page")
    @allure.title("Test cart page performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_page_performance(self):
        """Test cart page performance with items"""
        # First add items to cart
        product_page = ProductPage(self.page)
        product_page.navigate(f"{self.config.base_url}/product/1")
        product_page.add_to_cart()
        
        # Then measure cart page load
        thresholds = {
            "page_load_time": 2000,
            "first_contentful_paint": 1000
        }
        
        result = self.performance_test.measure_page_load(f"{self.config.base_url}/cart")
        self.performance_test.assert_performance_threshold(thresholds)