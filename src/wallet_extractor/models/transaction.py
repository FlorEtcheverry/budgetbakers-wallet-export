"""
Transaction model for wallet data representation.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime


@dataclass
class Transaction:
    """
    Represents a financial transaction from BudgetBakers Wallet.
    
    Attributes:
        category: Transaction category (e.g., "Groceries", "Savings")
        account: Account name (e.g., "Société Générale")
        amount: Transaction amount (e.g., "-€500.00")
        description: Transaction description/reference
        payee: Merchant or payee name
        labels: List of custom labels/tags
        date: Formatted date (DD/MM/YYYY)
        transaction_type: Type of transaction (Income, Expense, Transfer)
        raw_date: Original date text from HTML
    """
    category: str
    account: str
    amount: str
    description: str
    payee: str
    labels: List[str]
    date: str
    transaction_type: str
    raw_date: str
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            "category": self.category,
            "account": self.account,
            "amount": self.amount,
            "description": self.description,
            "payee": self.payee,
            "labels": self.labels,
            "date": self.date,
            "type": self.transaction_type,
            "raw_date": self.raw_date
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Create transaction from dictionary."""
        return cls(
            category=data.get("category", ""),
            account=data.get("account", ""),
            amount=data.get("amount", ""),
            description=data.get("description", ""),
            payee=data.get("payee", ""),
            labels=data.get("labels", []),
            date=data.get("date", ""),
            transaction_type=data.get("type", ""),
            raw_date=data.get("raw_date", "")
        )
    
    def is_expense(self) -> bool:
        """Check if transaction is an expense."""
        return self.transaction_type == "Expense"
    
    def is_income(self) -> bool:
        """Check if transaction is income."""
        return self.transaction_type == "Income"
    
    def is_transfer(self) -> bool:
        """Check if transaction is a transfer."""
        return self.transaction_type == "Transfer"
    
    def has_payee(self) -> bool:
        """Check if transaction has a payee."""
        return bool(self.payee.strip())
    
    def has_labels(self) -> bool:
        """Check if transaction has labels."""
        return bool(self.labels)
