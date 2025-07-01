"""
WebDriver management for Selenium automation.
"""

import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Optional


class DriverManager:
    """
    Manages WebDriver instances for browser automation.
    """
    
    def __init__(self, geckodriver_path: str, firefox_binary_path: Optional[str] = None, headless: bool = True):
        """
        Initialize driver manager.
        
        Args:
            geckodriver_path: Path to geckodriver executable
            firefox_binary_path: Path to Firefox binary (optional)
            headless: Whether to run in headless mode
        """
        self.geckodriver_path = geckodriver_path
        self.firefox_binary_path = firefox_binary_path
        self.headless = headless
        self._driver = None
    
    def create_driver(self) -> webdriver.Firefox:
        """
        Create and configure Firefox WebDriver.
        
        Returns:
            Configured Firefox WebDriver instance
        """
        service = Service(executable_path=self.geckodriver_path)
        options = FirefoxOptions()
        
        if self.firefox_binary_path:
            options.binary_location = self.firefox_binary_path
        
        if self.headless:
            options.add_argument("--headless")
        
        self._driver = webdriver.Firefox(service=service, options=options)
        return self._driver
    
    def get_driver(self) -> webdriver.Firefox:
        """
        Get existing driver or create new one.
        
        Returns:
            Firefox WebDriver instance
        """
        if self._driver is None:
            return self.create_driver()
        return self._driver
    
    def close_driver(self):
        """Close the WebDriver instance."""
        if self._driver:
            self._driver.close()
            self._driver = None
    
    def __enter__(self):
        """Context manager entry."""
        return self.get_driver()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_driver()


def create_default_driver_manager() -> DriverManager:
    """
    Create driver manager with default configuration for macOS.
    
    Returns:
        Configured DriverManager instance
    """
    geckodriver_path = "../geckodriver/geckodriver"
    firefox_binary_path = "/Applications/Firefox.app/Contents/MacOS/firefox"
    
    return DriverManager(
        geckodriver_path=geckodriver_path,
        firefox_binary_path=firefox_binary_path,
        headless=True
    )
