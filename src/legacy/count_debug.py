import os
from config import *
from selenium.webdriver.common.by import By
import time

if __name__ == "__main__":
    driver = configuration()
    try:
        print(f"Loading file: {FILE_PATH}")
        driver.get("file://" + FILE_PATH)
        
        # Wait a moment for the page to load
        time.sleep(2)
        
        # Find the main container
        els = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
        divs = els.find_elements(By.TAG_NAME, "div")
        print(f"Total div elements in container: {len(divs)}")
        
        # Count transaction elements across all divs
        total_transactions = 0
        divs_with_transactions = 0
        divs_with_dates = 0
        
        for i, div in enumerate(divs):
            try:
                # Try to find date elements
                date_elem = div.find_element(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP")
                divs_with_dates += 1
                if i < 10:  # Show first 10 dates
                    print(f"Date found in div {i}: {date_elem.text}")
            except:
                pass
            
            # Try to find transaction elements
            try:
                transactions = div.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                if transactions:
                    divs_with_transactions += 1
                    total_transactions += len(transactions)
                    if i < 10:  # Show details for first 10 divs with transactions
                        print(f"Div {i}: {len(transactions)} transactions")
            except:
                pass
        
        print(f"\nSummary:")
        print(f"Total divs: {len(divs)}")
        print(f"Divs with dates: {divs_with_dates}")
        print(f"Divs with transactions: {divs_with_transactions}")
        print(f"Total transactions found: {total_transactions}")
        
        # Check if there are any other transaction-like elements with different selectors
        all_possible_transactions = driver.find_elements(By.CSS_SELECTOR, "[class*='transaction'], [class*='Transaction'], [class*='entry'], [class*='Entry']")
        print(f"Other possible transaction elements: {len(all_possible_transactions)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()
