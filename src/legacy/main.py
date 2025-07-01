import os
import json

from contextlib import redirect_stdout
from config import *
from selenium.webdriver.common.by import By


if __name__ == "__main__":
    driver = configuration()
    driver.get("file://" + FILE_PATH )
    #els = driver.find_elements(By.CSS_SELECTOR, '._3wwqabSSUyshePYhPywONa')
    els = driver.find_element(By.CSS_SELECTOR, ".VypTY5DQ_tmahm5VdHFJK")
    
    els = els.find_elements(By.TAG_NAME, "div")
    cont = 0
    date = ""
    ach = True
    
    # Store all transactions in a list
    transactions = []

    for el in els:
        if cont > 5:
            try:
                date = el.find_element(By.CSS_SELECTOR, ".MhNEgOnlVNRo3U-Ti1ZHP").text
                ach = True
            except:
                ach = False
            
            elements = el.find_elements(By.CSS_SELECTOR, '._3wwqabSSUyshePYhPywONa')
            #print(date)
            for ele in elements:
                text = []
                data ={
                    "category": "",
                    "account": "",
                    "amount": 0,
                    "description": "",
                    "date": ""
                }
                text = ele.text.split("\n")
                if len(text) == 3:
                    data["category"] = text[0]
                    data["account"] = text[1]
                    data["amount"] = text[2]
                if len(text) == 4:
                    data["category"] = text[0]
                    data["account"] = text[1]
                    data["description"] = text[2]
                    data["amount"] = text[3]
                if len(text) == 5:
                    data["category"] = text[0]
                    data["account"] = text[1]
                    data["description"] = text[2] + " " + text[3]
                    data["amount"] = text[4]
                data["date"] = date
                transactions.append(data)
        cont = cont+1
    
    # Write proper JSON
    with open('../export/out.json', 'w', encoding="utf-8") as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    
    print(f"Exported {len(transactions)} transactions to out.json")
    driver.close()
    