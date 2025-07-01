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
        
        print("=== SEARCHING FOR PAYEE ELEMENTS ===")
        # Search for payee elements
        try:
            payee_elements = main_container.find_elements(By.CSS_SELECTOR, "._1HvfM2PHFVj--6nRBLVJIb")
            print(f"Found {len(payee_elements)} payee elements")
            
            for i, elem in enumerate(payee_elements[:5]):
                print(f"  Payee {i+1}: '{elem.text}'")
                
        except Exception as e:
            print(f"Error finding payee elements: {e}")
        
        print("\n=== SEARCHING FOR LABEL ELEMENTS ===")
        # Search for label elements  
        try:
            label_elements = main_container.find_elements(By.CSS_SELECTOR, "._2yWsrOsWf0KGrXIxhhDI2I")
            print(f"Found {len(label_elements)} label elements")
            
            for i, elem in enumerate(label_elements[:10]):
                print(f"  Label {i+1}: '{elem.text}'")
                
        except Exception as e:
            print(f"Error finding label elements: {e}")
        
        print("\n=== CHECKING TRANSACTION STRUCTURE ===")
        # Check if these elements are within transaction elements
        try:
            transactions = main_container.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
            print(f"Found {len(transactions)} transaction elements")
            
            # Check first few transactions for payee and labels
            for i, trans in enumerate(transactions[:3]):
                print(f"\nTransaction {i+1}:")
                print(f"  Text: {trans.text[:100]}...")
                
                # Look for payee within this transaction
                try:
                    payee_elem = trans.find_element(By.CSS_SELECTOR, "._1HvfM2PHFVj--6nRBLVJIb")
                    print(f"  Found payee: '{payee_elem.text}'")
                except:
                    print(f"  No payee found in this transaction")
                
                # Look for labels within this transaction
                try:
                    label_elems = trans.find_elements(By.CSS_SELECTOR, "._2yWsrOsWf0KGrXIxhhDI2I")
                    if label_elems:
                        labels = [elem.text for elem in label_elems]
                        print(f"  Found labels: {labels}")
                    else:
                        print(f"  No labels found in this transaction")
                except:
                    print(f"  Error finding labels in this transaction")
                    
        except Exception as e:
            print(f"Error processing transactions: {e}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.close()
