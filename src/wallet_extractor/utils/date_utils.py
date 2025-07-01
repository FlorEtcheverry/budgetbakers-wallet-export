"""
Date utility functions for transaction processing.
"""

from datetime import datetime
from typing import Dict


def parse_date_with_year(date_text: str, year: int = 2025) -> str:
    """
    Convert relative/partial dates to DD/MM/YYYY format.
    
    Args:
        date_text: Date text like 'Today', 'June 27', etc.
        year: Year to use for dates without year
        
    Returns:
        Formatted date string in DD/MM/YYYY format
    """
    if date_text.lower() == 'today':
        return datetime.now().strftime('%d/%m/%Y')
    
    months: Dict[str, str] = {
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
    except Exception:
        pass
    
    return date_text  # Return original if parsing fails


def determine_transaction_type(amount_text: str, description: str) -> str:
    """
    Determine transaction type based on amount and description.
    
    Args:
        amount_text: Amount string (e.g., "-€500.00")
        description: Transaction description
        
    Returns:
        Transaction type: "Income", "Expense", or "Transfer"
    """
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
