#!/bin/bash

echo "Installing Python dependencies..."

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Playwright system dependencies (for Linux)
playwright install-deps

echo "Installation complete!"