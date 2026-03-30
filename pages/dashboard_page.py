from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class DashboardPage(BasePage):
    """Dashboard page after successful login"""
    
    # Locators
    WELCOME_MESSAGE = ".welcome-message"
    USER_AVATAR = ".user-avatar"
    RECENT_ORDERS = ".recent-orders"
    PRODUCT_GRID = ".product-grid"
    SEARCH_INPUT = "input[name='search']"
    SEARCH_BUTTON = "button[type='submit']"
    LOGOUT_BUTTON = "a[href*='logout']"
    STATS_CARDS = ".stats-card"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Verify login success")
    def verify_login_success(self) -> None:
        """Verify that login was successful by checking welcome message"""
        self.verify_element_present(self.WELCOME_MESSAGE)
    
    @allure.step("Get welcome message")
    def get_welcome_message(self) -> str:
        """Get the welcome message text"""
        return self.get_text(self.WELCOME_MESSAGE)
    
    @allure.step("Search for product: {search_term}")
    def search_product(self, search_term: str) -> None:
        """Search for a product from dashboard"""
        self.fill(self.SEARCH_INPUT, search_term)
        self.click(self.SEARCH_BUTTON)
    
    @allure.step("Logout")
    def logout(self) -> None:
        """Logout from the application"""
        self.click(self.USER_AVATAR)
        self.click(self.LOGOUT_BUTTON)
    
    @allure.step("Click on user avatar")
    def click_avatar(self) -> None:
        """Click on user avatar to open menu"""
        self.click(self.USER_AVATAR)
    
    @allure.step("Get stats cards count")
    def get_stats_cards_count(self) -> int:
        """Get number of stats cards displayed"""
        cards = self.get_all_elements(self.STATS_CARDS)
        return len(cards)
    
    @allure.step("Get recent orders count")
    def get_recent_orders_count(self) -> int:
        """Get number of recent orders displayed"""
        orders = self.get_all_elements(self.RECENT_ORDERS)
        return len(orders)
    
    @allure.step("Verify dashboard loaded")
    def verify_dashboard_loaded(self) -> None:
        """Verify all dashboard elements are loaded"""
        self.verify_element_present(self.WELCOME_MESSAGE)
        self.verify_element_present(self.PRODUCT_GRID)