#!/usr/bin/env python3
"""
Main CLI script for wallet extraction.

Usage:
    python extract_wallet.py [--input INPUT_FILE] [--output OUTPUT_FILE] [--headless]
"""

import argparse
import os
import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wallet_extractor.core import WalletExtractor, create_default_driver_manager


def main():
    """Main CLI function."""
    _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    parser = argparse.ArgumentParser(
        description="Extract transaction data from BudgetBakers Wallet HTML files"
    )
    
    parser.add_argument(
        "--input", "-i",
        default=os.path.join(_ROOT, "site", "Wallet by BudgetBakers.html"),
        help="Path to input HTML file"
    )
    
    parser.add_argument(
        "--output", "-o", 
        default=os.path.join(_ROOT, "export", "transactions.json"),
        help="Path to output JSON file"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Extracting transactions from: {input_path}")
    print(f"Output will be saved to: {output_path}")
    
    try:
        # Detect format: only start a browser for legacy HTML
        with open(input_path, "r", encoding="utf-8") as f:
            head = f.read(4096)
        needs_browser = "mantine" not in head and "grid-cols-record-row" not in head

        driver_ctx = None
        driver = None
        if needs_browser:
            driver_manager = create_default_driver_manager()
            driver_ctx = driver_manager
            driver = driver_ctx.__enter__()

        try:
            extractor = WalletExtractor(driver)
            extractor.load_html_file(input_path)

            print("Extracting transactions...")
            transactions = extractor.extract_transactions()

            extractor.save_to_json(output_path)

            stats = extractor.get_statistics()
            print(f"\nExtraction completed successfully!")
            print(f"Statistics:")
            print(f"   Total transactions: {stats['total_transactions']}")
            print(f"   Income: {stats['income_transactions']}")
            print(f"   Expenses: {stats['expense_transactions']}")
            print(f"   Transfers: {stats['transfer_transactions']}")
            print(f"   With payee: {stats['transactions_with_payee']} ({stats['payee_coverage']})")
            print(f"   With labels: {stats['transactions_with_labels']} ({stats['label_coverage']})")

            if args.verbose:
                print(f"\nSample transactions:")
                for i, transaction in enumerate(transactions[:3]):
                    print(f"   {i+1}. {transaction.date} | {transaction.transaction_type} | {transaction.category} | {transaction.amount}")
                    if transaction.payee:
                        print(f"      Payee: {transaction.payee}")
                    if transaction.labels:
                        print(f"      Labels: {', '.join(transaction.labels)}")
        finally:
            if driver_ctx:
                driver_ctx.__exit__(None, None, None)

        return 0

    except Exception as e:
        print(f"Error during extraction: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
