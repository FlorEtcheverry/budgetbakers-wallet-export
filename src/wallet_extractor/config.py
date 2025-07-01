"""
Configuration settings for wallet extractor.
"""

import os
from pathlib import Path


class Config:
    """Configuration class for wallet extractor."""
    
    # File paths
    DEFAULT_HTML_FILE = "Wallet by BudgetBakers.html"
    DEFAULT_OUTPUT_FILE = "transactions.json"
    
    # Browser settings
    FIREFOX_BINARY_PATH = "/Applications/Firefox.app/Contents/MacOS/firefox"
    GECKODRIVER_PATH = "../geckodriver/geckodriver"
    
    # CSS selectors
    MAIN_CONTAINER_SELECTOR = ".VypTY5DQ_tmahm5VdHFJK"
    TRANSACTION_SELECTOR = "._3wwqabSSUyshePYhPywONa"
    DATE_SELECTOR = ".MhNEgOnlVNRo3U-Ti1ZHP"
    PAYEE_SELECTOR = "._1HvfM2PHFVj--6nRBLVJIb"
    LABEL_SELECTOR = "._2yWsrOsWf0KGrXIxhhDI2I"
    
    # Extraction settings
    SKIP_INITIAL_DIVS = 5
    DEFAULT_YEAR = 2025
    
    @classmethod
    def get_site_path(cls) -> str:
        """Get the default site directory path."""
        return os.path.abspath("../site")
    
    @classmethod
    def get_export_path(cls) -> str:
        """Get the default export directory path."""
        return os.path.abspath("../export")
    
    @classmethod
    def get_default_html_path(cls) -> str:
        """Get the default HTML file path."""
        return os.path.join(cls.get_site_path(), cls.DEFAULT_HTML_FILE)
    
    @classmethod
    def get_default_output_path(cls) -> str:
        """Get the default output file path."""
        return os.path.join(cls.get_export_path(), cls.DEFAULT_OUTPUT_FILE)
