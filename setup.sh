#!/bin/bash
# Setup script for downloading geckodriver

set -e

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo "Detected OS: $OS"

# Create geckodriver directory
mkdir -p geckodriver
cd geckodriver

# Download appropriate geckodriver
GECKODRIVER_VERSION="v0.34.0"
echo "Downloading geckodriver $GECKODRIVER_VERSION for $OS..."

case $OS in
    "linux")
        curl -L -o geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz"
        ;;
    "macos")
        curl -L -o geckodriver.tar.gz "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-macos.tar.gz"
        ;;
    "windows")
        curl -L -o geckodriver.zip "https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-win64.zip"
        ;;
    *)
        echo "Unsupported OS: $OSTYPE"
        echo "Please manually download geckodriver from: https://github.com/mozilla/geckodriver/releases"
        exit 1
        ;;
esac

# Extract
if [[ $OS == "windows" ]]; then
    unzip geckodriver.zip
    rm geckodriver.zip
else
    tar -xzf geckodriver.tar.gz
    rm geckodriver.tar.gz
fi

# Make executable (Linux/macOS)
if [[ $OS != "windows" ]]; then
    chmod +x geckodriver
fi

echo "✅ geckodriver installed successfully in geckodriver/ directory"
echo "📋 Next steps:"
echo "   1. Make sure Firefox is installed"
echo "   2. Install Python dependencies: pip install -r requirements.txt"
echo "   3. Run extraction: cd src && python extract_wallet.py"
