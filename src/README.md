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
├── extract_wallet.py         # Main CLI script
└── legacy/                   # Legacy files (moved here)
    ├── main.py
    ├── config.py
    └── debug_*.py
```

## 🚀 Usage

### Basic Usage

```bash
cd src
python extract_wallet.py
```

### Advanced Usage

```bash
# Custom input/output files
python extract_wallet.py --input /path/to/wallet.html --output /path/to/output.json

# Verbose output
python extract_wallet.py --verbose

# Convert to CSV
python scripts/json_to_csv.py --input ../export/transactions.json --output ../export/transactions.csv
```

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
