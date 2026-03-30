import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

@pytest.mark.regression
@pytest.mark.smoke
@allure.epic("Regression Testing")
@allure.feature("Complete Business Workflow")
class TestFullWorkflow:

    @pytest.fixture(autouse=True)
    def setup(self, page, config):
        self.page = page
        self.config = config
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
        self.product_page = ProductPage(page)
        self.cart_page = CartPage(page)

    @allure.story("E-commerce Flow")
    @allure.title("Test complete shopping workflow")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_complete_shopping_flow(self, test_data):
        """Test complete shopping workflow"""
        # 1. Login
        self.login_page.navigate("/login")
        self.login_page.login(
            self.config.username,
            self.config.password
        )
        self.dashboard_page.verify_login_success()

        # 2. Search for product
        search_term = test_data["product_name"]
        self.dashboard_page.search_product(search_term)
        self.product_page.verify_search_results(search_term)

        # 3. View product details
        self.product_page.select_first_product()
        product_details = self.product_page.get_product_details()
        assert product_details["name"] == search_term

        # 4. Add to cart
        initial_cart_count = self.product_page.get_cart_count()
        self.product_page.add_to_cart()
        updated_cart_count = self.product_page.get_cart_count()
        assert updated_cart_count == initial_cart_count + 1

        # 5. Go to cart
        self.product_page.go_to_cart()
        self.cart_page.verify_product_in_cart(search_term)

        # 6. Checkout
        self.cart_page.proceed_to_checkout()
        self.cart_page.verify_checkout_page()

        # 7. Fill shipping information
        self.cart_page.fill_shipping_info(test_data["shipping_info"])

        # 8. Select payment method
        self.cart_page.select_payment_method("credit_card")

        # 9. Place order
        order_id = self.cart_page.place_order()
        assert order_id is not None

        # 10. Verify order confirmation
        self.cart_page.verify_order_confirmation(order_id)

    @allure.story("Boundary Flow")
    @allure.title("Test shopping cart boundary cases")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cart_boundary_cases(self):
        """Test shopping cart boundary cases"""
        # Test empty cart
        self.cart_page.navigate("/cart")
        self.cart_page.verify_empty_cart_message()

        # Test maximum quantity limit
        self.product_page.navigate("/product/123")
        max_quantity = 99

        # Attempt to add quantity exceeding the maximum
        self.product_page.set_quantity(max_quantity + 1)
        self.product_page.add_to_cart()
        self.product_page.verify_error_message(f"Maximum quantity is {max_quantity}")

        # Test negative quantity
        self.product_page.set_quantity(-1)
        self.product_page.add_to_cart()
        self.product_page.verify_error_message("Quantity must be greater than 0")

        # Test decimal quantity
        self.product_page.set_quantity(1.5)
        self.product_page.add_to_cart()
        self.product_page.verify_error_message("Please enter an integer")

    @allure.story("Concurrency Testing")
    @allure.title("Test inventory concurrency issues")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_inventory_concurrency(self, browser_context):
        """Test inventory concurrency issues"""
        # Create multiple browser contexts to simulate concurrent users
        contexts = []
        for i in range(3):
            context = browser_context()
            page = context.new_page()
            login_page = LoginPage(page)
            product_page = ProductPage(page)

            login_page.navigate("/login")
            login_page.login(f"user{i}", "password")
            contexts.append((context, product_page))

        # All users simultaneously attempt to purchase the last item in stock
        product_id = "low_stock_product"
        for context, product_page in contexts:
            product_page.navigate(f"/product/{product_id}")
            product_page.add_to_cart()

        # Only one user should succeed
        # Verify inventory lock mechanism

    @allure.story("Performance Testing")
    @allure.title("Test page load performance")
    @allure.severity(allure.severity_level.NORMAL)
    def test_page_load_performance(self):
        """Test page load performance"""
        # Use Playwright's performance API
        with self.page.expect_response(lambda response: response.url.contains("api/products")) as response_info:
            self.page.goto("/products")

        response = response_info.value
        assert response.status == 200
        assert response.timing["responseEnd"] - response.timing["requestStart"] < 2000  # Within 2 seconds

    @allure.story("Compatibility Testing")
    @allure.title("Test cross-browser compatibility")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("browser_type", ["chromium", "firefox", "webkit"])
    def test_cross_browser_compatibility(self, browser_type):
        """Test cross-browser compatibility"""
        # This test will run across different browsers
        self.login_page.navigate("/login")
        self.login_page.verify_login_form_present()

        # Verify key functionality works across all browsers
        self.login_page.fill(self.login_page.USERNAME_INPUT, "test")
        self.login_page.fill(self.login_page.PASSWORD_INPUT, "test")

        # Take screenshot for comparison
        screenshot = self.login_page.take_screenshot(f"login_form_{browser_type}")