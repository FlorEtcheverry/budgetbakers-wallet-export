# Export Directory

This directory contains the extracted transaction data in JSON and CSV formats.

## Generated Files

- `transactions.json` - Main JSON export from the extraction tool
- `transactions.csv` - CSV format for Excel/spreadsheet applications  
- `out_enhanced.json` - Enhanced extraction with full date parsing
- Other temporary/debug output files

## Security Note

⚠️ **This directory is excluded from Git** to protect your financial data.
The extracted files contain your personal transaction information and should never be committed to version control.

## Usage

Run the extraction tools from the `src/` directory:

```bash
cd src
python fast_extract.py              # Fast extraction
python extract_wallet.py           # Professional extraction
python scripts/json_to_csv.py      # Convert JSON to CSV
```
