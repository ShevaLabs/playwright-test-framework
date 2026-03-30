from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class ProductPage(BasePage):
    """Product listing and details page"""
    
    # Locators
    PRODUCT_TITLE = ".product-title"
    PRODUCT_PRICE = ".product-price"
    PRODUCT_DESCRIPTION = ".product-description"
    ADD_TO_CART_BUTTON = "button.add-to-cart"
    QUANTITY_INPUT = "input[name='quantity']"
    CART_COUNT = ".cart-count"
    PRODUCT_IMAGE = ".product-image"
    REVIEWS_SECTION = ".reviews"
    RATING_STARS = ".rating-stars"
    AVAILABLE_STOCK = ".stock-count"
    RELATED_PRODUCTS = ".related-products"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Get product details")
    def get_product_details(self) -> dict:
        """Get product details from product page"""
        return {
            "name": self.get_text(self.PRODUCT_TITLE),
            "price": self.get_text(self.PRODUCT_PRICE),
            "description": self.get_text(self.PRODUCT_DESCRIPTION),
            "stock": self.get_text(self.AVAILABLE_STOCK)
        }
    
    @allure.step("Set quantity: {quantity}")
    def set_quantity(self, quantity: int) -> None:
        """Set product quantity"""
        self.clear_input(self.QUANTITY_INPUT)
        self.fill(self.QUANTITY_INPUT, str(quantity))
    
    @allure.step("Add to cart")
    def add_to_cart(self) -> None:
        """Add current product to cart"""
        self.click(self.ADD_TO_CART_BUTTON)
    
    @allure.step("Get cart count")
    def get_cart_count(self) -> int:
        """Get current cart item count"""
        count_text = self.get_text(self.CART_COUNT)
        try:
            return int(count_text)
        except (ValueError, TypeError):
            return 0
    
    @allure.step("Verify search results for: {search_term}")
    def verify_search_results(self, search_term: str) -> None:
        """Verify search results contain expected term"""
        self.verify_text_present(self.PRODUCT_TITLE, search_term)
    
    @allure.step("Select first product")
    def select_first_product(self) -> None:
        """Click on the first product in listing"""
        first_product = ".product-item:first-child"
        self.click(first_product)
    
    @allure.step("Go to cart")
    def go_to_cart(self) -> None:
        """Navigate to cart page"""
        self.click(self.CART_COUNT)
    
    @allure.step("Verify error message: {expected_message}")
    def verify_error_message(self, expected_message: str) -> None:
        """Verify error message appears"""
        self.verify_text_present(".error-message", expected_message)
    
    @allure.step("Get product price")
    def get_product_price(self) -> float:
        """Get product price as float"""
        price_text = self.get_text(self.PRODUCT_PRICE)
        return float(price_text.replace('$', '').replace(',', ''))
    
    @allure.step("Get available stock")
    def get_available_stock(self) -> int:
        """Get available stock count"""
        stock_text = self.get_text(self.AVAILABLE_STOCK)
        return int(stock_text)