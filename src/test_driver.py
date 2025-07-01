#!/usr/bin/env python3
"""
Simple test script to debug extraction issues.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wallet_extractor.core import create_default_driver_manager

def test_driver():
    """Test driver creation and basic functionality."""
    print("1. Testing driver creation...")
    
    try:
        driver_manager = create_default_driver_manager()
        print("✓ Driver manager created")
        
        print("2. Testing driver initialization...")
        with driver_manager as driver:
            print("✓ Driver initialized")
            
            print("3. Testing page load...")
            input_path = os.path.abspath("../site/Wallet by BudgetBakers.html")
            
            if not os.path.exists(input_path):
                print(f"✗ HTML file not found: {input_path}")
                return False
            
            driver.get(f"file://{input_path}")
            print("✓ Page loaded")
            
            print("4. Testing basic element finding...")
            from selenium.webdriver.common.by import By
            
            # Try to find the main container
            try:
                main_container = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
                print("✓ Main container found")
                
                divs = main_container.find_elements(By.TAG_NAME, "div")
                print(f"✓ Found {len(divs)} div elements")
                
                if len(divs) > 10:
                    print("✓ Sufficient divs for processing")
                    return True
                else:
                    print("✗ Not enough divs found")
                    return False
                    
            except Exception as e:
                print(f"✗ Error finding elements: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Error during test: {e}")
        return False

if __name__ == "__main__":
    success = test_driver()
    if success:
        print("\n✅ All tests passed! Driver is working correctly.")
    else:
        print("\n❌ Tests failed! There's an issue with the driver setup.")
    
    sys.exit(0 if success else 1)
