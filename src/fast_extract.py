#!/usr/bin/env python3
"""
Fast extraction script using the legacy approach but with improvements.
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wallet_extractor.core import create_default_driver_manager
from selenium.webdriver.common.by import By

def parse_date_with_year(date_text, year=2025):
    """Convert relative/partial dates to DD/MM/YYYY format."""
    if date_text.lower() == 'today':
        return datetime.now().strftime('%d/%m/%Y')
    
    months = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }
    
    try:
        parts = date_text.lower().split()
        if len(parts) == 2:
            month_name, day = parts
            month_num = months.get(month_name, '01')
            return f"{day.zfill(2)}/{month_num}/{year}"
    except:
        pass
    
    return date_text

def determine_transaction_type(amount_text, description):
    """Determine transaction type based on amount and description."""
    if amount_text.startswith('-'):
        if 'VIR' in description and ('POUR:' in description or 'PERM' in description):
            return 'Transfer'
        else:
            return 'Expense'
    else:
        if 'VIR' in description and 'REC' in description:
            return 'Income'
        else:
            return 'Income'

def fast_extract():
    """Fast extraction using simplified approach."""
    print("Starting fast extraction...")
    
    try:
        driver_manager = create_default_driver_manager()
        
        with driver_manager as driver:
            input_path = os.path.abspath("../site/Wallet by BudgetBakers.html")
            output_path = os.path.abspath("../export/transactions_fast.json")
            
            print(f"Loading: {input_path}")
            driver.get(f"file://{input_path}")
            
            # Find main container
            main_container = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
            divs = main_container.find_elements(By.TAG_NAME, "div")
            
            print(f"Found {len(divs)} divs, processing...")
            
            transactions = []
            current_date = ""
            
            for i, div in enumerate(divs):
                if i > 5:  # Skip first few divs
                    if i % 1000 == 0:
                        print(f"Processed {i}/{len(divs)} divs, found {len(transactions)} transactions")
                    
                    # Try to find date element
                    try:
                        date_element = div.find_element(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP")
                        current_date = date_element.text
                    except:
                        pass
                    
                    # Find transaction elements in this div
                    try:
                        transaction_elements = div.find_elements(By.CSS_SELECTOR, "._3wwqabSSUyshePYhPywONa")
                        
                        for trans_elem in transaction_elements:
                            text_lines = trans_elem.text.split("\n")
                            
                            if len(text_lines) >= 3:
                                # Parse basic data
                                transaction = {
                                    "category": "",
                                    "account": "",
                                    "amount": "",
                                    "description": "",
                                    "payee": "",
                                    "labels": [],
                                    "date": parse_date_with_year(current_date),
                                    "type": "",
                                    "raw_date": current_date
                                }
                                
                                # Parse text lines
                                if len(text_lines) == 3:
                                    transaction["category"] = text_lines[0]
                                    transaction["account"] = text_lines[1].strip()
                                    transaction["amount"] = text_lines[2]
                                elif len(text_lines) == 4:
                                    transaction["category"] = text_lines[0]
                                    transaction["account"] = text_lines[1].strip()
                                    transaction["description"] = text_lines[2]
                                    transaction["amount"] = text_lines[3]
                                elif len(text_lines) >= 5:
                                    transaction["category"] = text_lines[0]
                                    transaction["account"] = text_lines[1].strip()
                                    transaction["description"] = " ".join(text_lines[2:-1])
                                    transaction["amount"] = text_lines[-1]
                                
                                # Quick payee extraction (no deep searching)
                                try:
                                    payee_elem = trans_elem.find_element(By.CSS_SELECTOR, "._1HvfM2PHFVj--6nRBLVJIb")
                                    transaction["payee"] = payee_elem.text.strip()
                                except:
                                    pass
                                
                                # Quick label extraction
                                try:
                                    label_elems = trans_elem.find_elements(By.CSS_SELECTOR, "._2yWsrOsWf0KGrXIxhhDI2I")
                                    transaction["labels"] = [elem.text.strip() for elem in label_elems if elem.text.strip()]
                                except:
                                    pass
                                
                                # Determine type
                                transaction["type"] = determine_transaction_type(transaction["amount"], transaction["description"])
                                
                                transactions.append(transaction)
                    except:
                        pass
            
            print(f"\nExtraction completed! Found {len(transactions)} transactions")
            
            # Save to JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transactions, f, indent=2, ensure_ascii=False)
            
            print(f"Saved to: {output_path}")
            
            # Statistics
            with_payee = len([t for t in transactions if t['payee']])
            with_labels = len([t for t in transactions if t['labels']])
            
            print(f"\nStatistics:")
            print(f"  Total: {len(transactions)}")
            print(f"  With payee: {with_payee} ({with_payee/len(transactions)*100:.1f}%)")
            print(f"  With labels: {with_labels} ({with_labels/len(transactions)*100:.1f}%)")
            
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = fast_extract()
    sys.exit(0 if success else 1)
