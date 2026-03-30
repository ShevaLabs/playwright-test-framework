from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class Header(BasePage):
    """Header component with navigation elements"""
    
    # Locators
    LOGO = ".logo"
    SEARCH_INPUT = "input[type='search']"
    SEARCH_BUTTON = "button[type='submit']"
    CART_ICON = ".cart-icon"
    USER_MENU = ".user-menu"
    LOGOUT_LINK = "a[href*='logout']"
    WISHLIST_ICON = ".wishlist-icon"
    NOTIFICATION_BELL = ".notification-bell"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Click on logo")
    def click_logo(self) -> None:
        """Click on the logo to return to home page"""
        self.click(self.LOGO)
    
    @allure.step("Search for product: {search_term}")
    def search(self, search_term: str) -> None:
        """Perform a search for a product"""
        self.fill(self.SEARCH_INPUT, search_term)
        self.click(self.SEARCH_BUTTON)
    
    @allure.step("Go to cart")
    def go_to_cart(self) -> None:
        """Navigate to shopping cart"""
        self.click(self.CART_ICON)
    
    @allure.step("Open user menu")
    def open_user_menu(self) -> None:
        """Open the user dropdown menu"""
        self.click(self.USER_MENU)
    
    @allure.step("Logout")
    def logout(self) -> None:
        """Perform logout action"""
        self.open_user_menu()
        self.click(self.LOGOUT_LINK)
    
    @allure.step("Go to wishlist")
    def go_to_wishlist(self) -> None:
        """Navigate to wishlist"""
        self.click(self.WISHLIST_ICON)
    
    @allure.step("Get cart count")
    def get_cart_count(self) -> int:
        """Get the number of items in cart"""
        cart_count_text = self.get_text(self.CART_ICON)
        try:
            return int(cart_count_text)
        except (ValueError, TypeError):
            return 0
    
    @allure.step("Verify user is logged in")
    def verify_logged_in(self) -> None:
        """Verify that user is logged in by checking user menu exists"""
        self.verify_element_present(self.USER_MENU)