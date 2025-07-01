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
        
        # Get first few payee and label elements to understand their context
        print("=== ANALYZING PAYEE ELEMENT STRUCTURE ===")
        try:
            payee_elements = main_container.find_elements(By.CSS_SELECTOR, "._1HvfM2PHFVj--6nRBLVJIb")
            
            for i, payee_elem in enumerate(payee_elements[:3]):
                print(f"\nPayee {i+1}: '{payee_elem.text}'")
                
                # Check parent elements to understand structure
                parent = payee_elem.find_element(By.XPATH, "..")
                print(f"  Parent HTML: {parent.get_attribute('outerHTML')[:200]}...")
                
                # Check if there are transaction elements nearby
                try:
                    # Look for transaction elements in parent or siblings
                    transaction_in_parent = parent.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                    if transaction_in_parent:
                        print(f"  Found {len(transaction_in_parent)} transaction elements in parent")
                    else:
                        # Check grandparent
                        grandparent = parent.find_element(By.XPATH, "..")
                        transaction_in_grandparent = grandparent.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                        if transaction_in_grandparent:
                            print(f"  Found {len(transaction_in_grandparent)} transaction elements in grandparent")
                        else:
                            print(f"  No transaction elements found in parent/grandparent")
                except Exception as e:
                    print(f"  Error checking for related transactions: {e}")
                    
        except Exception as e:
            print(f"Error analyzing payee structure: {e}")
        
        print("\n=== ANALYZING LABEL ELEMENT STRUCTURE ===")
        try:
            label_elements = main_container.find_elements(By.CSS_SELECTOR, "._2yWsrOsWf0KGrXIxhhDI2I")
            
            for i, label_elem in enumerate(label_elements[:3]):
                print(f"\nLabel {i+1}: '{label_elem.text}'")
                
                # Check parent elements to understand structure
                parent = label_elem.find_element(By.XPATH, "..")
                print(f"  Parent HTML: {parent.get_attribute('outerHTML')[:200]}...")
                
                # Check if there are transaction elements nearby
                try:
                    # Look for transaction elements in parent or siblings
                    transaction_in_parent = parent.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                    if transaction_in_parent:
                        print(f"  Found {len(transaction_in_parent)} transaction elements in parent")
                    else:
                        # Check grandparent
                        grandparent = parent.find_element(By.XPATH, "..")
                        transaction_in_grandparent = grandparent.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                        if transaction_in_grandparent:
                            print(f"  Found {len(transaction_in_grandparent)} transaction elements in grandparent")
                        else:
                            print(f"  No transaction elements found in parent/grandparent")
                except Exception as e:
                    print(f"  Error checking for related transactions: {e}")
                    
        except Exception as e:
            print(f"Error analyzing label structure: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
