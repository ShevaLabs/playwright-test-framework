Write-Host "Installing Python dependencies..."

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate

# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install

Write-Host "Installation complete!"