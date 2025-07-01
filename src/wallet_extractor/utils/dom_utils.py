"""
DOM parsing utilities for extracting transaction data.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from typing import List, Tuple


def extract_payee_and_labels(trans_elem: WebElement) -> Tuple[str, List[str]]:
    """
    Extract payee and labels from transaction element and its context.
    
    Args:
        trans_elem: Transaction WebElement
        
    Returns:
        Tuple of (payee, labels)
    """
    payee = ""
    labels: List[str] = []
    
    # Define search contexts: transaction element, parent, grandparent only
    search_contexts = [trans_elem]
    try:
        parent = trans_elem.find_element(By.XPATH, "..")
        search_contexts.append(parent)
        # Skip grandparent for now to improve performance
    except Exception:
        pass
    
    # Search for payee in all contexts
    for context in search_contexts:
        if not payee:  # Only search if we haven't found a payee yet
            try:
                payee_elem = context.find_element(By.CSS_SELECTOR, "._1HvfM2PHFVj--6nRBLVJIb")
                payee = payee_elem.text.strip()
                break  # Found payee, stop searching
            except Exception:
                pass
    
    # Search for labels in all contexts
    for context in search_contexts:
        if not labels:  # Only search if we haven't found labels yet
            try:
                label_elements = context.find_elements(By.CSS_SELECTOR, "._2yWsrOsWf0KGrXIxhhDI2I")
                labels = [elem.text.strip() for elem in label_elements if elem.text.strip()]
                if labels:  # Found labels, stop searching
                    break
            except Exception:
                pass
    
    return payee, labels


def parse_transaction_text_lines(text_lines: List[str]) -> Tuple[str, str, str, str]:
    """
    Parse transaction text lines into structured data.
    
    Args:
        text_lines: List of text lines from transaction element
        
    Returns:
        Tuple of (category, account, description, amount)
    """
    category = ""
    account = ""
    description = ""
    amount = ""
    
    if len(text_lines) == 3:
        category = text_lines[0]
        account = text_lines[1].strip()
        amount = text_lines[2]
    elif len(text_lines) == 4:
        category = text_lines[0]
        account = text_lines[1].strip()
        description = text_lines[2]
        amount = text_lines[3]
    elif len(text_lines) >= 5:
        category = text_lines[0]
        account = text_lines[1].strip()
        description = " ".join(text_lines[2:-1])
        amount = text_lines[-1]
    
    return category, account, description, amount
