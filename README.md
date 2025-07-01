# BudgetBakers Wallet Export Tool

A professional-grade tool for extracting transaction data from BudgetBakers Wallet HTML export files without requiring a premium account.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Firefox browser installed
- BudgetBakers Wallet HTML export file

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd budgetbakers-wallet-export
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download geckodriver (automated):
```bash
./setup.sh
```

   **Or manually:**
   - Download geckodriver from [Mozilla releases](https://github.com/mozilla/geckodriver/releases)
   - Extract to `geckodriver/` directory
   - Make executable: `chmod +x geckodriver/geckodriver`

4. Save your Wallet HTML export:
   - Go to BudgetBakers Wallet web interface
   - Navigate to your transactions page
   - **Scroll down to load ALL transactions** (important!)
   - Save page as HTML (Ctrl+S / Cmd+S)
   - Place the HTML file in the `site/` directory

### Usage

#### Fast Extraction (Recommended)
```bash
cd src
python fast_extract.py
```

#### Professional CLI Tool
```bash
cd src
python extract_wallet.py --verbose
```

#### Convert to CSV
```bash
cd src
python scripts/json_to_csv.py
```

## 📊 Features

- ✅ **Complete Transaction Data**: Category, account, amount, description, payee, labels
- ✅ **Multiple Formats**: Export to JSON and CSV
- ✅ **Full Date Parsing**: Converts relative dates to DD/MM/YYYY format
- ✅ **Transaction Classification**: Automatically categorizes as Income/Expense/Transfer
- ✅ **Professional Code Structure**: Clean, modular, and maintainable
- ✅ **Progress Tracking**: Real-time extraction progress
- ✅ **Privacy First**: Data directories excluded from Git

## 🏗️ Project Structure

```
├── src/                           # Source code
│   ├── wallet_extractor/          # Main package
│   │   ├── core/                  # Core functionality
│   │   ├── models/                # Data models
│   │   ├── utils/                 # Utility functions
│   │   └── config.py              # Configuration
│   ├── scripts/                   # Utility scripts
│   ├── extract_wallet.py          # Professional CLI
│   ├── fast_extract.py           # Fast extraction
│   └── legacy/                    # Original implementation
├── site/                          # HTML export files (excluded from Git)
├── export/                        # Generated data files (excluded from Git)
├── geckodriver/                   # Browser driver (excluded from Git)
└── requirements.txt               # Python dependencies
```

## 📈 Extraction Statistics

The tool provides detailed statistics:
- Total transactions extracted (~3,800+ typical)
- Payee coverage (~44% with merchant/payee info)
- Label coverage (~20% with custom labels)
- Transaction type breakdown (Income/Expense/Transfer)

## 🔧 Configuration

Key settings in `src/wallet_extractor/config.py`:
- CSS selectors for different elements
- Browser and driver paths
- Default file locations

## 🛡️ Privacy & Security

- ⚠️ **Data directories (`site/`, `export/`, `geckodriver/`) are excluded from Git**
- Never commit personal financial information
- All extraction happens locally on your machine
- No data is sent to external services

## 📝 Legacy vs New Implementation

- **Legacy**: `src/main.py` - Original implementation
- **New**: `src/fast_extract.py` - Optimized for performance
- **Professional**: `src/extract_wallet.py` - Full-featured CLI tool

## 🤝 Contributing

This is a fork/improvement of the original BudgetBakers wallet export tool, restructured for better maintainability and performance.

## 📄 License

MIT License - See original project for licensing details.
