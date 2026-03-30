import pytest
from playwright.sync_api import sync_playwright
from typing import Dict, Any
import allure

@pytest.fixture(scope="session")
def playwright_instance():
    """Create playwright instance"""
    with sync_playwright() as playwright:
        yield playwright

@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    """Create browser instance based on configuration"""
    playwright_config = config.get_playwright_config()
    browser_type = playwright_config.get("browser", "chromium")
    headless = playwright_config.get("headless", False)
    slow_mo = playwright_config.get("slow_mo", 0)
    
    browser_instance = getattr(playwright_instance, browser_type)
    
    browser = browser_instance.launch(
        headless=headless,
        slow_mo=slow_mo
    )
    
    yield browser
    
    browser.close()

@pytest.fixture
def browser_context_args(browser, config):
    """Browser context arguments"""
    playwright_config = config.get_playwright_config()
    viewport = playwright_config.get("viewport", {"width": 1920, "height": 1080})
    
    return {
        "viewport": viewport,
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }

@pytest.fixture
def browser_context(browser, browser_context_args):
    """Create browser context"""
    context = browser.new_context(**browser_context_args)
    yield context
    context.close()