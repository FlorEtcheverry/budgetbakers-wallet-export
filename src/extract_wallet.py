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
    parser = argparse.ArgumentParser(
        description="Extract transaction data from BudgetBakers Wallet HTML files"
    )
    
    parser.add_argument(
        "--input", "-i",
        default="../site/Wallet by BudgetBakers.html",
        help="Path to input HTML file (default: ../site/Wallet by BudgetBakers.html)"
    )
    
    parser.add_argument(
        "--output", "-o", 
        default="../export/transactions.json",
        help="Path to output JSON file (default: ../export/transactions.json)"
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
        # Create driver manager and extractor
        driver_manager = create_default_driver_manager()
        
        with driver_manager as driver:
            extractor = WalletExtractor(driver)
            
            # Load HTML file
            extractor.load_html_file(input_path)
            
            # Extract transactions
            print("Extracting transactions...")
            transactions = extractor.extract_transactions()
            
            # Save to JSON
            extractor.save_to_json(output_path)
            
            # Print statistics
            stats = extractor.get_statistics()
            print(f"\n✅ Extraction completed successfully!")
            print(f"📊 Statistics:")
            print(f"   • Total transactions: {stats['total_transactions']}")
            print(f"   • Income: {stats['income_transactions']}")
            print(f"   • Expenses: {stats['expense_transactions']}")
            print(f"   • Transfers: {stats['transfer_transactions']}")
            print(f"   • With payee: {stats['transactions_with_payee']} ({stats['payee_coverage']})")
            print(f"   • With labels: {stats['transactions_with_labels']} ({stats['label_coverage']})")
            
            if args.verbose:
                print(f"\n📝 Sample transactions:")
                for i, transaction in enumerate(transactions[:3]):
                    print(f"   {i+1}. {transaction.date} | {transaction.type} | {transaction.category} | {transaction.amount}")
                    if transaction.payee:
                        print(f"      Payee: {transaction.payee}")
                    if transaction.labels:
                        print(f"      Labels: {', '.join(transaction.labels)}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during extraction: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
