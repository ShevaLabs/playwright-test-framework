"""
Action Performance Tests
"""
import pytest
import allure
from tests.performance.performance_base import PerformanceTestBase
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.performance_monitor import PerformanceMonitor, LoadTestSimulator


@pytest.mark.performance
@allure.epic("Performance Testing")
@allure.feature("Action Performance")
class TestActionPerformance:
    
    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.page = page
        self.config = config
        self.performance_test = PerformanceTestBase(page)
        self.monitor = PerformanceMonitor()
        
        # Login first for authenticated actions
        login_page = LoginPage(page)
        login_page.navigate(f"{self.config.base_url}/login")
        login_page.login(self.config.username, self.config.password)
    
    @allure.story("Login Action")
    @allure.title("Test login action performance")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_action_performance(self):
        """Test login action response time"""
        login_page = LoginPage(self.page)
        
        def perform_login():
            login_page.fill(login_page.USERNAME_INPUT, self.config.username)
            login_page.fill(login_page.PASSWORD_INPUT, self.config.password)
            login_page.click(login_page.LOGIN_BUTTON)
            self.page.wait_for_load_state("networkidle")
        
        action_time, _ = self.performance_test.measure_action_performance(
            perform_login, "login_action"
        )
        
        assert action_time < 2000, f"Login action took {action_time}ms, expected < 2000ms"
    
    @allure.story("Search Action")
    @allure.title("Test search action performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_action_performance(self):
        """Test search action response time"""
        dashboard_page = DashboardPage(self.page)
        
        def perform_search():
            dashboard_page.search_product("test product")
        
        action_time, _ = self.performance_test.measure_action_performance(
            perform_search, "search_action"
        )
        
        assert action_time < 1000, f"Search action took {action_time}ms, expected < 1000ms"
    
    @allure.story("Add to Cart Action")
    @allure.title("Test add to cart action performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_to_cart_performance(self):
        """Test add to cart action response time"""
        product_page = ProductPage(self.page)
        product_page.navigate(f"{self.config.base_url}/product/1")
        
        def add_to_cart():
            product_page.add_to_cart()
        
        action_time, _ = self.performance_test.measure_action_performance(
            add_to_cart, "add_to_cart_action"
        )
        
        assert action_time < 500, f"Add to cart action took {action_time}ms, expected < 500ms"
    
    @allure.story("Checkout Action")
    @allure.title("Test checkout action performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_action_performance(self):
        """Test checkout action response time"""
        cart_page = CartPage(self.page)
        cart_page.navigate(f"{self.config.base_url}/cart")
        
        def proceed_to_checkout():
            cart_page.proceed_to_checkout()
        
        action_time, _ = self.performance_test.measure_action_performance(
            proceed_to_checkout, "checkout_action"
        )
        
        assert action_time < 1500, f"Checkout action took {action_time}ms, expected < 1500ms"
    
    @allure.story("Rendering Performance")
    @allure.title("Test element rendering performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_element_rendering_performance(self):
        """Test rendering time for specific elements"""
        dashboard_page = DashboardPage(self.page)
        dashboard_page.navigate(f"{self.config.base_url}/dashboard")
        
        # Measure rendering performance for product grid
        rendering_metrics = self.performance_test.measure_rendering_performance(".product-grid")
        
        assert rendering_metrics["element_appear_time_ms"] < 2000
        assert rendering_metrics["element_render_time_ms"] < 100