import os
from config import *
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":
    driver = configuration()
    try:
        print(f"Loading file: {FILE_PATH}")
        driver.get("file://" + FILE_PATH)
        
        time.sleep(2)
        
        # Find the main container
        main_container = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
        
        # Count all transaction elements directly
        all_transactions = main_container.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
        print(f"Total transaction elements found: {len(all_transactions)}")
        
        # Count date elements
        all_dates = main_container.find_elements(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP")
        print(f"Total date elements found: {len(all_dates)}")
        
        # Sample a few transactions to see their content
        print("\nSample transactions:")
        for i, trans in enumerate(all_transactions[:5]):
            print(f"Transaction {i+1}: {trans.text[:100]}...")
            
        # Check if there are other potential transaction selectors
        print("\nChecking for other potential transaction elements...")
        
        # Look for elements with similar patterns
        other_selectors = [
            "[class*='transaction']",
            "[class*='Transaction']", 
            "[class*='record']",
            "[class*='Record']",
            "[class*='entry']",
            "[class*='Entry']"
        ]
        
        for selector in other_selectors:
            try:
                elements = main_container.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"Found {len(elements)} elements with selector: {selector}")
            except:
                pass
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
