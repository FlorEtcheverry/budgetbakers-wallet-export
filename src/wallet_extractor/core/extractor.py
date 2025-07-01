"""
Main wallet data extractor class.
"""

import json
from typing import List, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from ..models.transaction import Transaction
from ..utils.date_utils import parse_date_with_year, determine_transaction_type
from ..utils.dom_utils import extract_payee_and_labels, parse_transaction_text_lines


class WalletExtractor:
    """
    Main class for extracting transaction data from BudgetBakers Wallet HTML files.
    """
    
    # CSS selectors for various elements
    MAIN_CONTAINER_SELECTOR = ".VypTY5DQ_tmahm5VdHFJK"
    TRANSACTION_SELECTOR = "._3wwqabSSUyshePYhPywONa"
    DATE_SELECTOR = ".MhNEgOnlVNRo3U-Ti1ZHP"
    
    def __init__(self, driver: WebDriver):
        """
        Initialize extractor with WebDriver.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.transactions: List[Transaction] = []
    
    def load_html_file(self, file_path: str):
        """
        Load HTML file in the browser.
        
        Args:
            file_path: Absolute path to the HTML file
        """
        self.driver.get(f"file://{file_path}")
    
    def extract_transactions(self, skip_divs: int = 5) -> List[Transaction]:
        """
        Extract all transactions from the loaded HTML.
        
        Args:
            skip_divs: Number of initial divs to skip
            
        Returns:
            List of Transaction objects
        """
        self.transactions = []
        
        try:
            # Find main container
            main_container = self.driver.find_element(By.CSS_SELECTOR, self.MAIN_CONTAINER_SELECTOR)
            
            # More efficient approach: find all transaction elements first
            print("Finding all transaction elements...")
            all_transaction_elements = main_container.find_elements(By.CSS_SELECTOR, self.TRANSACTION_SELECTOR)
            print(f"Found {len(all_transaction_elements)} transaction elements")
            
            # Process each transaction element
            for i, trans_elem in enumerate(all_transaction_elements):
                if i % 500 == 0:  # Progress indicator
                    print(f"Processing transaction {i+1}/{len(all_transaction_elements)}...")
                
                # Find the date for this transaction by looking at parent elements
                current_date = self._find_date_for_transaction(trans_elem)
                
                transaction = self._extract_single_transaction(trans_elem, current_date)
                if transaction:
                    self.transactions.append(transaction)
            
        except Exception as e:
            raise RuntimeError(f"Failed to extract transactions: {e}")
        
        return self.transactions
    
    def _find_date_for_transaction(self, trans_elem) -> str:
        """
        Find the date associated with a transaction element.
        
        Args:
            trans_elem: Transaction WebElement
            
        Returns:
            Date string or empty string if not found
        """
        # Search in parent elements for date (limit search depth for performance)
        current = trans_elem
        for _ in range(3):  # Search up to 3 levels up (reduced from 5)
            try:
                parent = current.find_element(By.XPATH, "..")
                
                # Look for date element in this parent
                try:
                    date_elem = parent.find_element(By.CSS_SELECTOR, self.DATE_SELECTOR)
                    return date_elem.text
                except Exception:
                    pass
                
                current = parent
            except Exception:
                break
        
        return "Unknown"
    
    def _extract_single_transaction(self, trans_elem, current_date: str) -> Optional[Transaction]:
        """
        Extract a single transaction from a transaction element.
        
        Args:
            trans_elem: Transaction WebElement
            current_date: Current date context
            
        Returns:
            Transaction object or None if extraction fails
        """
        try:
            text_lines = trans_elem.text.split("\n")
            
            if len(text_lines) < 3:
                return None
            
            # Parse basic transaction data
            category, account, description, amount = parse_transaction_text_lines(text_lines)
            
            # Extract payee and labels
            payee, labels = extract_payee_and_labels(trans_elem)
            
            # Create transaction object
            transaction = Transaction(
                category=category,
                account=account,
                amount=amount,
                description=description,
                payee=payee,
                labels=labels,
                date=parse_date_with_year(current_date),
                transaction_type=determine_transaction_type(amount, description),
                raw_date=current_date
            )
            
            return transaction
            
        except Exception:
            return None
    
    def save_to_json(self, output_path: str, indent: int = 2):
        """
        Save extracted transactions to JSON file.
        
        Args:
            output_path: Path to output JSON file
            indent: JSON indentation level
        """
        transaction_dicts = [t.to_dict() for t in self.transactions]
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(transaction_dicts, f, indent=indent, ensure_ascii=False)
    
    def get_statistics(self) -> dict:
        """
        Get statistics about extracted transactions.
        
        Returns:
            Dictionary with extraction statistics
        """
        total = len(self.transactions)
        with_payee = len([t for t in self.transactions if t.has_payee()])
        with_labels = len([t for t in self.transactions if t.has_labels()])
        
        income_count = len([t for t in self.transactions if t.is_income()])
        expense_count = len([t for t in self.transactions if t.is_expense()])
        transfer_count = len([t for t in self.transactions if t.is_transfer()])
        
        return {
            "total_transactions": total,
            "transactions_with_payee": with_payee,
            "transactions_with_labels": with_labels,
            "income_transactions": income_count,
            "expense_transactions": expense_count,
            "transfer_transactions": transfer_count,
            "payee_coverage": f"{(with_payee/total*100):.1f}%" if total > 0 else "0%",
            "label_coverage": f"{(with_labels/total*100):.1f}%" if total > 0 else "0%"
        }
