"""
Page Object Model module
"""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage",
    "ProductPage",
    "CartPage"
]