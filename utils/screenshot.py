import os
from pathlib import Path
from datetime import datetime
from playwright.sync_api import Page
import allure

class ScreenshotHelper:
    """Helper class for taking screenshots"""
    
    def __init__(self, page: Page, screenshot_dir: str = "./screenshots"):
        self.page = page
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def capture(self, name: str = None, full_page: bool = True) -> str:
        """
        Take a screenshot and save to file
        
        Args:
            name: Screenshot name (without extension)
            full_page: Whether to capture full page scroll
        
        Returns:
            Path to the saved screenshot file
        """
        if not name:
            name = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        # Ensure filename has .png extension
        if not name.endswith('.png'):
            name = f"{name}.png"
        
        screenshot_path = self.screenshot_dir / name
        self.page.screenshot(path=str(screenshot_path), full_page=full_page)
        
        return str(screenshot_path)
    
    def capture_element(self, selector: str, name: str = None) -> str:
        """
        Take a screenshot of a specific element
        
        Args:
            selector: CSS selector for the element
            name: Screenshot name
        
        Returns:
            Path to the saved screenshot file
        """
        if not name:
            name = f"element_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        if not name.endswith('.png'):
            name = f"{name}.png"
        
        screenshot_path = self.screenshot_dir / name
        element = self.page.locator(selector).first
        element.screenshot(path=str(screenshot_path))
        
        return str(screenshot_path)
    
    def capture_and_attach(self, name: str = None, full_page: bool = True) -> None:
        """
        Take screenshot and attach to Allure report
        
        Args:
            name: Screenshot name
            full_page: Whether to capture full page
        """
        screenshot_path = self.capture(name, full_page)
        
        with open(screenshot_path, 'rb') as f:
            allure.attach(
                f.read(),
                name=name or "screenshot",
                attachment_type=allure.attachment_type.PNG
            )
    
    def capture_comparison(self, before_name: str, after_name: str) -> dict:
        """
        Take before and after screenshots for comparison
        
        Args:
            before_name: Name for before screenshot
            after_name: Name for after screenshot
        
        Returns:
            Dictionary with paths to both screenshots
        """
        before_path = self.capture(f"{before_name}_before")
        after_path = self.capture(f"{after_name}_after")
        
        return {
            "before": before_path,
            "after": after_path
        }