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
        
        # Check if there are multiple containers or sections
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        print(f"Total divs on page: {len(all_divs)}")
        
        # Look for elements that contain financial data patterns
        elements_with_euro = driver.find_elements(By.XPATH, "//*[contains(text(), '€')]")
        print(f"Elements containing '€': {len(elements_with_euro)}")
        
        elements_with_minus_euro = driver.find_elements(By.XPATH, "//*[contains(text(), '-€')]")
        print(f"Elements containing '-€': {len(elements_with_minus_euro)}")
        
        elements_with_plus_euro = driver.find_elements(By.XPATH, "//*[contains(text(), '+€')]")
        print(f"Elements containing '+€': {len(elements_with_plus_euro)}")
        
        # Check for other common currency patterns
        elements_with_decimal = driver.find_elements(By.XPATH, "//*[contains(text(), '.') and (contains(text(), '€') or contains(text(), '$'))]")
        print(f"Elements with decimal currency: {len(elements_with_decimal)}")
        
        # Look for the main container differently
        containers = driver.find_elements(By.CSS_SELECTOR, "[class*='VypTY5DQ']")
        print(f"Containers with VypTY5DQ class: {len(containers)}")
        
        if containers:
            main_container = containers[0]
            # Try different selectors for transaction-like elements
            selectors_to_try = [
                "._3wwqabSSUyshePYhPywONa",  # Original selector
                "[class*='3wwqab']",         # Partial match
                "[class*='wwqab']",          # Even more partial
                "div[class*='_']",           # Any div with underscore classes
            ]
            
            for selector in selectors_to_try:
                try:
                    elements = main_container.find_elements(By.CSS_SELECTOR, selector)
                    print(f"Selector '{selector}': {len(elements)} elements")
                    
                    # Check if these elements contain currency
                    currency_elements = 0
                    for elem in elements:
                        if '€' in elem.text:
                            currency_elements += 1
                    print(f"  - Elements with currency: {currency_elements}")
                except Exception as e:
                    print(f"Selector '{selector}' failed: {e}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            driver.close()
        except:
            pass
