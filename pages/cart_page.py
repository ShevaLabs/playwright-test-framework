from pages.base_page import BasePage
from playwright.sync_api import Page
import allure

class CartPage(BasePage):
    """Shopping cart page"""
    
    # Locators
    CART_ITEMS = ".cart-item"
    ITEM_QUANTITY = ".item-quantity"
    ITEM_PRICE = ".item-price"
    ITEM_TOTAL = ".item-total"
    CART_TOTAL = ".cart-total"
    CHECKOUT_BUTTON = "button.checkout"
    REMOVE_ITEM_BUTTON = ".remove-item"
    EMPTY_CART_MESSAGE = ".empty-cart-message"
    PROMO_CODE_INPUT = "input[name='promo']"
    APPLY_PROMO_BUTTON = "button.apply-promo"
    SHIPPING_COST = ".shipping-cost"
    TAX_AMOUNT = ".tax-amount"
    GRAND_TOTAL = ".grand-total"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    @allure.step("Verify product in cart: {product_name}")
    def verify_product_in_cart(self, product_name: str) -> None:
        """Verify specific product exists in cart"""
        self.verify_text_present(self.CART_ITEMS, product_name)
    
    @allure.step("Proceed to checkout")
    def proceed_to_checkout(self) -> None:
        """Click checkout button"""
        self.click(self.CHECKOUT_BUTTON)
    
    @allure.step("Verify checkout page")
    def verify_checkout_page(self) -> None:
        """Verify checkout page loaded"""
        self.wait_for_url("**/checkout")
    
    @allure.step("Fill shipping information")
    def fill_shipping_info(self, shipping_info: dict) -> None:
        """Fill shipping information form"""
        self.fill("input[name='first_name']", shipping_info.get("first_name", ""))
        self.fill("input[name='last_name']", shipping_info.get("last_name", ""))
        self.fill("input[name='address']", shipping_info.get("address", ""))
        self.fill("input[name='city']", shipping_info.get("city", ""))
        self.fill("input[name='postal_code']", shipping_info.get("postal_code", ""))
        self.select_dropdown_option("select[name='country']", shipping_info.get("country", ""))
    
    @allure.step("Select payment method: {method}")
    def select_payment_method(self, method: str) -> None:
        """Select payment method"""
        payment_option = f"input[value='{method}']"
        self.click(payment_option)
    
    @allure.step("Place order")
    def place_order(self) -> str:
        """Place order and return order ID"""
        order_button = "button.place-order"
        self.click(order_button)
        
        # Wait for order confirmation and get order ID
        self.wait_for_element(".order-id")
        order_id = self.get_text(".order-id")
        return order_id
    
    @allure.step("Verify order confirmation: {order_id}")
    def verify_order_confirmation(self, order_id: str) -> None:
        """Verify order confirmation page with order ID"""
        self.verify_text_present(".confirmation-message", order_id)
    
    @allure.step("Verify empty cart message")
    def verify_empty_cart_message(self) -> None:
        """Verify empty cart message is displayed"""
        self.verify_element_present(self.EMPTY_CART_MESSAGE)
    
    @allure.step("Remove item from cart")
    def remove_item(self, item_index: int = 0) -> None:
        """Remove item from cart by index"""
        remove_buttons = self.get_all_elements(self.REMOVE_ITEM_BUTTON)
        if remove_buttons and item_index < len(remove_buttons):
            remove_buttons[item_index].click()
    
    @allure.step("Update item quantity: {quantity}")
    def update_quantity(self, quantity: int, item_index: int = 0) -> None:
        """Update quantity for cart item"""
        quantity_inputs = self.get_all_elements(self.ITEM_QUANTITY)
        if quantity_inputs and item_index < len(quantity_inputs):
            quantity_inputs[item_index].fill(str(quantity))
            quantity_inputs[item_index].press("Enter")
    
    @allure.step("Apply promo code: {promo_code}")
    def apply_promo_code(self, promo_code: str) -> None:
        """Apply promo code to cart"""
        self.fill(self.PROMO_CODE_INPUT, promo_code)
        self.click(self.APPLY_PROMO_BUTTON)
    
    @allure.step("Get cart total")
    def get_cart_total(self) -> float:
        """Get cart total amount"""
        total_text = self.get_text(self.GRAND_TOTAL)
        return float(total_text.replace('$', '').replace(',', ''))
    
    @allure.step("Get cart item count")
    def get_cart_item_count(self) -> int:
        """Get number of items in cart"""
        items = self.get_all_elements(self.CART_ITEMS)
        return len(items)