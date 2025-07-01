import os
from config import *
from selenium.webdriver.common.by import By
import time
import re

if __name__ == "__main__":
    driver = configuration()
    try:
        print(f"Loading file: {FILE_PATH}")
        driver.get("file://" + FILE_PATH)
        
        time.sleep(2)
        
        # Find the main container
        main_container = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
        
        # Look for different date formats
        print("=== SEARCHING FOR DATE PATTERNS ===")
        
        # Search for elements containing specific months
        month_patterns = ["June", "May", "April", "March", "February", "January"]
        for month in month_patterns:
            try:
                elements = main_container.find_elements(By.XPATH, f"//*[contains(text(), '{month}')]")
                if elements:
                    print(f"\nFound {len(elements)} elements containing '{month}':")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        print(f"  {i+1}. Text: '{elem.text}' | Class: '{elem.get_attribute('class')}'")
                        # Check if parent has more context
                        parent = elem.find_element(By.XPATH, "..")
                        print(f"     Parent text: '{parent.text[:100]}...'")
            except Exception as e:
                print(f"Error searching for {month}: {e}")
        
        print("\n=== SEARCHING FOR TRANSACTION TYPES ===")
        
        # Search for transaction type elements
        type_patterns = ["Income", "Expense", "Transfer"]
        for trans_type in type_patterns:
            try:
                elements = main_container.find_elements(By.XPATH, f"//*[contains(text(), '{trans_type}')]")
                if elements:
                    print(f"\nFound {len(elements)} elements containing '{trans_type}':")
                    for i, elem in enumerate(elements[:3]):  # Show first 3
                        print(f"  {i+1}. Text: '{elem.text}' | Class: '{elem.get_attribute('class')}'")
                        # Check siblings for transaction details
                        parent = elem.find_element(By.XPATH, "..")
                        print(f"     Parent text: '{parent.text[:150]}...'")
            except Exception as e:
                print(f"Error searching for {trans_type}: {e}")
                
        print("\n=== LOOKING FOR PAYEE/MERCHANT INFO ===")
        
        # Look for common payee patterns (card transactions, transfers, etc.)
        payee_patterns = ["CARTE", "VIR", "PREL", "CHQ"]
        for pattern in payee_patterns:
            try:
                elements = main_container.find_elements(By.XPATH, f"//*[contains(text(), '{pattern}')]")
                if elements:
                    print(f"\nFound {len(elements)} elements containing '{pattern}':")
                    elem = elements[0]  # Just show first one
                    print(f"  Text: '{elem.text[:100]}...'")
                    print(f"  Class: '{elem.get_attribute('class')}'")
            except Exception as e:
                print(f"Error searching for {pattern}: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
