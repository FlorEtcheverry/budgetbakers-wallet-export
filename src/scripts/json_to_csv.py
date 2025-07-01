#!/usr/bin/env python3
"""
CSV converter script - converts JSON output to CSV format.
"""

import json
import csv
import argparse
import os
import sys


def json_to_csv(json_file: str, csv_file: str):
    """
    Convert JSON transactions to CSV format.
    
    Args:
        json_file: Path to input JSON file
        csv_file: Path to output CSV file
    """
    with open(json_file, 'r', encoding='utf-8') as f:
        transactions = json.load(f)
    
    if not transactions:
        print("No transactions found in JSON file")
        return
    
    # CSV headers
    headers = [
        'Date', 'Type', 'Category', 'Account', 'Amount', 
        'Description', 'Payee', 'Labels'
    ]
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for transaction in transactions:
            # Format labels as comma-separated string
            labels = ', '.join(transaction.get('labels', []))
            
            row = [
                transaction.get('date', ''),
                transaction.get('type', ''),
                transaction.get('category', ''),
                transaction.get('account', ''),
                transaction.get('amount', ''),
                transaction.get('description', ''),
                transaction.get('payee', ''),
                labels
            ]
            writer.writerow(row)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Convert JSON transaction data to CSV format"
    )
    
    parser.add_argument(
        "--input", "-i",
        default="../export/transactions.json",
        help="Path to input JSON file (default: ../export/transactions.json)"
    )
    
    parser.add_argument(
        "--output", "-o",
        default="../export/transactions.csv", 
        help="Path to output CSV file (default: ../export/transactions.csv)"
    )
    
    args = parser.parse_args()
    
    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}")
        return 1
    
    try:
        print(f"Converting {input_path} to {output_path}")
        json_to_csv(input_path, output_path)
        print("✅ CSV conversion completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
