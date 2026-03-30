from playwright.sync_api import Page, Locator
from typing import Callable, Optional, Any
import time
from utils.logger import logger

class WaitHelper:
    """Helper class for custom wait conditions"""
    
    def __init__(self, page: Page, default_timeout: int = 30000):
        self.page = page
        self.default_timeout = default_timeout
    
    def wait_for_condition(self, condition: Callable[[], bool], timeout: int = None, interval: int = 500) -> bool:
        """
        Wait for a condition to become True
        
        Args:
            condition: Function that returns boolean
            timeout: Maximum time to wait in milliseconds
            interval: Check interval in milliseconds
        
        Returns:
            True if condition met, False if timeout
        """
        timeout = timeout or self.default_timeout
        start_time = time.time() * 1000
        
        while (time.time() * 1000 - start_time) < timeout:
            if condition():
                return True
            time.sleep(interval / 1000)
        
        logger.warning(f"Condition not met within {timeout}ms")
        return False
    
    def wait_for_text_change(self, selector: str, initial_text: str, timeout: int = None) -> bool:
        """
        Wait for element text to change from initial value
        
        Args:
            selector: CSS selector
            initial_text: Initial text value
            timeout: Timeout in milliseconds
        
        Returns:
            True if text changed, False if timeout
        """
        def text_changed():
            current_text = self.page.locator(selector).first.text_content()
            return current_text != initial_text
        
        return self.wait_for_condition(text_changed, timeout)
    
    def wait_for_attribute(self, selector: str, attribute: str, value: str, timeout: int = None) -> bool:
        """
        Wait for element to have specific attribute value
        
        Args:
            selector: CSS selector
            attribute: Attribute name
            value: Expected attribute value
            timeout: Timeout in milliseconds
        
        Returns:
            True if attribute matches, False if timeout
        """
        def attribute_matches():
            element = self.page.locator(selector).first
            attr_value = element.get_attribute(attribute)
            return attr_value == value
        
        return self.wait_for_condition(attribute_matches, timeout)
    
    def wait_for_element_count(self, selector: str, expected_count: int, timeout: int = None) -> bool:
        """
        Wait for specific number of elements to appear
        
        Args:
            selector: CSS selector
            expected_count: Expected number of elements
            timeout: Timeout in milliseconds
        
        Returns:
            True if count matches, False if timeout
        """
        def count_matches():
            elements = self.page.locator(selector).all()
            return len(elements) == expected_count
        
        return self.wait_for_condition(count_matches, timeout)
    
    def wait_for_ajax_complete(self, timeout: int = None) -> None:
        """
        Wait for all AJAX requests to complete
        
        Args:
            timeout: Timeout in milliseconds
        """
        def ajax_complete():
            return self.page.evaluate("window.jQuery && jQuery.active == 0")
        
        self.wait_for_condition(ajax_complete, timeout)
    
    def wait_for_image_load(self, selector: str, timeout: int = None) -> bool:
        """
        Wait for image to be fully loaded
        
        Args:
            selector: CSS selector for image
            timeout: Timeout in milliseconds
        
        Returns:
            True if image loaded, False if timeout
        """
        def image_loaded():
            element = self.page.locator(selector).first
            return element.evaluate("element => element.complete")
        
        return self.wait_for_condition(image_loaded, timeout)
    
    def wait_for_animation(self, selector: str, timeout: int = 3000) -> None:
        """
        Wait for CSS animation to complete
        
        Args:
            selector: CSS selector
            timeout: Maximum wait time
        """
        self.page.wait_for_function(
            """
            selector => {
                const element = document.querySelector(selector);
                if (!element) return true;
                const animations = element.getAnimations();
                return Promise.all(animations.map(animation => animation.finished));
            }
            """,
            arg=selector,
            timeout=timeout
        )