#!/usr/bin/env python3
"""
Quick extraction test to diagnose performance issues.
"""

import os
import sys
import time

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wallet_extractor.core import create_default_driver_manager
from selenium.webdriver.common.by import By

def quick_test():
    """Quick test of extraction performance."""
    print("Starting quick extraction test...")
    
    try:
        driver_manager = create_default_driver_manager()
        
        with driver_manager as driver:
            input_path = os.path.abspath("../site/Wallet by BudgetBakers.html")
            
            print("Loading HTML file...")
            start_time = time.time()
            driver.get(f"file://{input_path}")
            print(f"✓ File loaded in {time.time() - start_time:.2f} seconds")
            
            print("Finding main container...")
            start_time = time.time()
            main_container = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
            print(f"✓ Main container found in {time.time() - start_time:.2f} seconds")
            
            print("Finding all transaction elements...")
            start_time = time.time()
            all_transactions = main_container.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
            print(f"✓ Found {len(all_transactions)} transactions in {time.time() - start_time:.2f} seconds")
            
            print("Testing single transaction extraction...")
            start_time = time.time()
            if all_transactions:
                trans = all_transactions[0]
                text = trans.text
                print(f"✓ Extracted text from first transaction in {time.time() - start_time:.2f} seconds")
                print(f"   First transaction text: {text[:100]}...")
            
            # Test processing a few transactions
            print("Testing batch processing (first 10 transactions)...")
            start_time = time.time()
            for i, trans in enumerate(all_transactions[:10]):
                text_lines = trans.text.split("\n")
                if len(text_lines) >= 3:
                    pass  # Just parse, don't do anything complex
            
            print(f"✓ Processed 10 transactions in {time.time() - start_time:.2f} seconds")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = quick_test()
    print(f"\n{'✅ Test completed successfully!' if success else '❌ Test failed!'}")
    sys.exit(0 if success else 1)
