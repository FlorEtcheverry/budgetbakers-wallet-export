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
        
        print(f"Page title: {driver.title}")
        print(f"Page source length: {len(driver.page_source)}")
        
        # Try to find the main container
        try:
            els = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
            print("Found main container with class .VypTY5DQ_tmahm5VdHFJK")
            
            # Get all divs in the container
            divs = els.find_elements(By.TAG_NAME, "div")
            print(f"Found {len(divs)} div elements in container")
            
            # Look for transaction elements
            for i, div in enumerate(divs[:10]):  # Check first 10 divs
                try:
                    # Try to find date elements
                    date_elem = div.find_element(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP")
                    print(f"Div {i}: Found date element with text: {date_elem.text}")
                except:
                    pass
                
                # Try to find transaction elements
                try:
                    transactions = div.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                    if transactions:
                        print(f"Div {i}: Found {len(transactions)} transaction elements")
                        for j, trans in enumerate(transactions[:3]):  # Check first 3 transactions
                            print(f"  Transaction {j}: {trans.text[:100]}...")
                except:
                    pass
            
        except Exception as e:
            print(f"Could not find .VypTY5DQ_tmahm5VdHFJK: {e}")
            
            # Let's look for any divs and see what classes are available
            all_divs = driver.find_elements(By.TAG_NAME, "div")
            print(f"Found {len(all_divs)} div elements")
            
            # Get unique class names
            classes = set()
            for div in all_divs[:50]:  # Check first 50 divs
                class_attr = div.get_attribute("class")
                if class_attr:
                    classes.update(class_attr.split())
            
            print("Some available classes:")
            for cls in sorted(classes)[:20]:
                print(f"  .{cls}")
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
