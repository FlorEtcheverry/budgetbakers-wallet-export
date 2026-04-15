"""
Date utility functions for transaction processing.
"""

from datetime import datetime
from typing import Dict


def parse_date_with_year(date_text: str, year: int = None) -> str:
    """
    Convert relative/partial dates to DD/MM/YYYY format.

    Handles three formats from the Wallet UI:
      - "Today"              → current date
      - "Month Day"          → day/month of the current year (e.g. "April 15")
      - "Month Day, Year"    → full date (e.g. "March 2, 2026")

    Args:
        date_text: Date text from the Wallet page header
        year: Year to use for 2-part dates without a year; defaults to current year

    Returns:
        Formatted date string in DD/MM/YYYY format
    """
    if year is None:
        year = datetime.now().year

    if date_text.lower() == 'today':
        return datetime.now().strftime('%d/%m/%Y')

    months: Dict[str, str] = {
        'january': '01', 'february': '02', 'march': '03', 'april': '04',
        'may': '05', 'june': '06', 'july': '07', 'august': '08',
        'september': '09', 'october': '10', 'november': '11', 'december': '12'
    }

    try:
        # Normalise: remove commas, then split
        parts = date_text.replace(',', '').lower().split()

        if len(parts) == 2:
            # "April 15"  →  no year in UI, use current/provided year
            month_name, day = parts
            month_num = months.get(month_name, '01')
            return f"{day.zfill(2)}/{month_num}/{year}"

        if len(parts) == 3:
            # "March 2, 2026"  →  full date with explicit year
            month_name, day, explicit_year = parts
            month_num = months.get(month_name, '01')
            return f"{day.zfill(2)}/{month_num}/{explicit_year}"

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
