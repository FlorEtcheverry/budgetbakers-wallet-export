"""
Wallet Export Tool - BudgetBakers Wallet HTML Export Parser

This package provides tools to extract transaction data from saved BudgetBakers 
Wallet HTML files and export them to JSON/CSV formats.

Author: Wallet Export Tool
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Wallet Export Tool"

from .core.extractor import WalletExtractor
from .core.driver_manager import DriverManager
from .models.transaction import Transaction

__all__ = ["WalletExtractor", "DriverManager", "Transaction"]
