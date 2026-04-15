# Professional Wallet Extractor

A professional-grade tool for extracting transaction data from BudgetBakers Wallet HTML export files.

## 🏗️ Project Structure

```
src/
├── wallet_extractor/           # Main package
│   ├── __init__.py            # Package initialization
│   ├── config.py              # Configuration settings
│   ├── core/                  # Core functionality
│   │   ├── __init__.py
│   │   ├── driver_manager.py  # WebDriver management
│   │   └── extractor.py       # Main extraction logic
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   └── transaction.py     # Transaction model
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── date_utils.py      # Date parsing utilities
│       └── dom_utils.py       # DOM parsing utilities
├── scripts/                   # Utility scripts
│   └── json_to_csv.py        # JSON to CSV converter
├── extract_wallet.py         # ✅ Recommended CLI script → exports/transactions.json
├── fast_extract.py           # Alternative fast extractor → export/transactions_fast.json
├── main.py                   # Original prototype → export/out.json (no date parsing)
├── main_enhanced.py          # Placeholder (empty)
├── quick_test.py             # Quick sanity-check script
├── test_driver.py            # WebDriver connectivity test
└── legacy/                   # Archived debug/analysis scripts
    ├── main.py
    ├── config.py
    └── (debug scripts)
```

## 🚀 Usage

### Recommended

```bash
cd src
python extract_wallet.py
```

Outputs → `export/transactions.json` with full date parsing, payee, labels, and type classification.

### Options

```bash
# Custom input/output paths
python extract_wallet.py --input /path/to/wallet.html --output /path/to/output.json

# Verbose output (shows sample transactions)
python extract_wallet.py --verbose

# Alternative fast extractor (same fields, slightly different DOM traversal)
python fast_extract.py   # → export/transactions_fast.json

# Convert JSON to CSV
python scripts/json_to_csv.py --input ../export/transactions.json --output ../export/transactions.csv
```

### Script Comparison

| Script | Output | Date parsing | Payee/Labels | Notes |
|---|---|---|---|---|
| `extract_wallet.py` | `transactions.json` | ✅ DD/MM/YYYY | ✅ | **Recommended** — full CLI, modular |
| `fast_extract.py` | `transactions_fast.json` | ✅ DD/MM/YYYY | ✅ | Same data, self-contained |
| `main.py` | `out.json` | ❌ raw string | ❌ | Original prototype, kept for reference |

## 📊 Features

- **Professional Code Structure**: Clean, modular, and maintainable codebase
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive error handling and logging
- **CLI Interface**: Easy-to-use command-line interface
- **Statistics**: Detailed extraction statistics
- **Multiple Formats**: Export to JSON and CSV
- **Flexible Configuration**: Configurable selectors and paths

## 🔧 Development

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run extraction with verbose output
python extract_wallet.py --verbose
```

### Code Quality

The codebase follows Python best practices:
- PEP 8 style guidelines
- Type hints throughout
- Docstrings for all classes and functions
- Modular design with clear separation of concerns

## 📈 Extraction Statistics

The tool provides detailed statistics about the extraction:
- Total transactions extracted
- Breakdown by type (Income/Expense/Transfer)
- Coverage statistics for payees and labels
- Sample transaction preview

## 🛠️ Configuration

Key configurations can be modified in `wallet_extractor/config.py`:
- CSS selectors for different elements
- Default file paths
- Browser settings
- Extraction parameters
