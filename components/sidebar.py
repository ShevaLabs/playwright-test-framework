from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class Sidebar(BasePage):
    """Sidebar component with navigation categories"""
    
    # Locators
    CATEGORY_LINKS = ".category-link"
    FILTER_SECTION = ".filter-section"
    PRICE_FILTER = ".price-filter"
    BRAND_FILTER = ".brand-filter"
    RATING_FILTER = ".rating-filter"
    APPLY_FILTERS_BUTTON = ".apply-filters"
    CLEAR_FILTERS_BUTTON = ".clear-filters"
    COLLAPSE_BUTTON = ".sidebar-collapse"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Select category: {category_name}")
    def select_category(self, category_name: str) -> None:
        """Select a category from the sidebar"""
        category_link = f"a:has-text('{category_name}')"
        self.click(category_link)
    
    @allure.step("Apply price filter: min={min_price}, max={max_price}")
    def apply_price_filter(self, min_price: int, max_price: int) -> None:
        """Apply price range filter"""
        self.fill("input[name='min_price']", str(min_price))
        self.fill("input[name='max_price']", str(max_price))
        self.click(self.APPLY_FILTERS_BUTTON)
    
    @allure.step("Select brand: {brand_name}")
    def select_brand(self, brand_name: str) -> None:
        """Select a brand filter"""
        brand_checkbox = f"input[value='{brand_name}']"
        self.click(brand_checkbox)
        self.click(self.APPLY_FILTERS_BUTTON)
    
    @allure.step("Select rating: {rating}")
    def select_rating(self, rating: int) -> None:
        """Select rating filter"""
        rating_checkbox = f"input[value='{rating}']"
        self.click(rating_checkbox)
        self.click(self.APPLY_FILTERS_BUTTON)
    
    @allure.step("Clear all filters")
    def clear_filters(self) -> None:
        """Clear all applied filters"""
        self.click(self.CLEAR_FILTERS_BUTTON)
    
    @allure.step("Collapse sidebar")
    def collapse(self) -> None:
        """Collapse the sidebar"""
        self.click(self.COLLAPSE_BUTTON)
    
    @allure.step("Get all categories")
    def get_all_categories(self) -> list:
        """Get list of all category names"""
        categories = self.get_all_elements(self.CATEGORY_LINKS)
        return [category.text_content() for category in categories]