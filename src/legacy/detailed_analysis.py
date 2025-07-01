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
        divs = main_container.find_elements(By.TAG_NAME, "div")
        
        print(f"Analyzing transaction structure...")
        
        # Look at a few transactions in detail
        for i, div in enumerate(divs[6:16]):  # Check divs 6-15
            print(f"\n=== DIV {i+6} ===")
            
            # Check for date elements
            try:
                date_elem = div.find_element(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP")
                print(f"Date element text: '{date_elem.text}'")
                
                # Look for parent elements that might contain full date
                parent = date_elem.find_element(By.XPATH, "..")
                print(f"Date parent HTML snippet: {parent.get_attribute('outerHTML')[:200]}...")
                
            except:
                pass
            
            # Check for transaction elements
            try:
                transactions = div.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                if transactions:
                    print(f"Found {len(transactions)} transactions in this div")
                    
                    # Examine first transaction in detail
                    trans = transactions[0]
                    print(f"Transaction text: {trans.text}")
                    print(f"Transaction HTML: {trans.get_attribute('outerHTML')[:300]}...")
                    
                    # Look for parent elements that might contain more info
                    parent = trans.find_element(By.XPATH, "..")
                    print(f"Transaction parent HTML: {parent.get_attribute('outerHTML')[:300]}...")
                    
                    # Look for siblings that might contain date, type, etc.
                    siblings = parent.find_elements(By.XPATH, "../*")
                    print(f"Found {len(siblings)} siblings")
                    for j, sibling in enumerate(siblings[:3]):
                        print(f"  Sibling {j}: {sibling.get_attribute('class')} - {sibling.text[:50]}...")
            except Exception as e:
                print(f"Error processing transactions: {e}")
                
            if i >= 5:  # Only check first few divs with content
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
