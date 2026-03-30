# Playwright Test Framework

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright Version](https://img.shields.io/badge/playwright-1.40.0-brightgreen.svg)](https://playwright.dev/)
[![Pytest Version](https://img.shields.io/badge/pytest-7.4.3-blue.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive, enterprise-ready test automation framework built with Playwright and Pytest, supporting UI automation, API testing, performance testing, and end-to-end workflows.

## 🚀 Features

- ✅ **UI Automation Testing** - Page Object Model design pattern with multi-browser support (Chromium, Firefox, WebKit)
- ✅ **API Testing** - Complete RESTful API testing capabilities with authentication handling
- ✅ **Performance Testing** - Page load time monitoring and API response time benchmarks
- ✅ **Data-Driven Testing** - YAML-based test data management with dynamic data generation
- ✅ **Parallel Execution** - Multi-threaded test execution for faster feedback
- ✅ **Comprehensive Reporting** - Allure and HTML reports with screenshots, videos, and logs
- ✅ **CI/CD Integration** - Ready-to-use configurations for Jenkins, GitLab CI, and GitHub Actions
- ✅ **Cross-Browser Testing** - Run tests across multiple browsers with the same codebase
- ✅ **Mobile Testing** - Mobile viewport simulation for responsive design testing
- ✅ **Visual Testing** - Screenshot capture and comparison capabilities
- ✅ **Error Handling** - Automatic retry mechanisms and failure screenshots
- ✅ **Logging System** - Comprehensive logging with console and file output

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Examples](#test-examples)
- [Generating Reports](#generating-reports)
- [CI/CD Integration](#cicd-integration)
- [Contributing](#contributing)
- [License](#license)

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for version control)
- Allure Command Line (optional, for Allure reports)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/playwright-test-framework.git
cd playwright-test-framework
```

### 2. Create Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Playwright system dependencies (Linux only)
playwright install-deps
```

### 4. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# .env file:
# PROD_USERNAME=your_prod_username
# PROD_PASSWORD=your_prod_password
```

## 📁 Project Structure

```text
playwright-test-framework/
├── config/                    # Configuration files
│   ├── __init__.py
│   ├── config.yaml           # Main configuration (browsers, timeouts, etc.)
│   ├── test_data.yaml        # Test data for data-driven tests
│   └── environment.py        # Environment configuration handler
│
├── pages/                     # Page Object Model
│   ├── __init__.py
│   ├── base_page.py          # Base page with common methods
│   ├── login_page.py         # Login page objects
│   ├── dashboard_page.py     # Dashboard page objects
│   ├── product_page.py       # Product page objects
│   └── cart_page.py          # Cart page objects
│
├── components/                # Reusable UI components
│   ├── __init__.py
│   ├── header.py             # Header component
│   ├── sidebar.py            # Sidebar component
│   └── modal.py              # Modal dialog component
│
├── tests/                     # Test cases
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures and hooks
│   ├── ui/                   # UI test cases
│   ├── api/                  # API test cases
│   ├── performance/          # Performance test cases
│   ├── boundary/             # Boundary test cases
│   ├── regression/           # Regression test cases
│   └── smoke/                # Smoke test cases
│
├── utils/                     # Utility classes
│   ├── __init__.py
│   ├── data_generator.py     # Test data generation
│   ├── logger.py             # Logging utilities
│   ├── report_generator.py   # Report generation
│   ├── screenshot.py         # Screenshot helper
│   ├── wait_helper.py        # Custom wait conditions
│   └── api_client.py         # API client for HTTP requests
│
├── fixtures/                  # Pytest fixtures
│   ├── __init__.py
│   ├── browser_fixture.py    # Browser and context fixtures
│   └── data_fixture.py       # Data fixtures
│
├── reports/                   # Test reports
│   ├── html/                 # HTML reports
│   └── allure-results/       # Allure raw data
│
├── logs/                      # Log files
├── screenshots/               # Failure screenshots
├── traces/                    # Playwright traces
├── requirements.txt           # Python dependencies
├── pytest.ini                # Pytest configuration
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore file
├── run_tests.py              # Test runner script
└── README.md                 # This file
```

## ⚙️ Configuration

### config/config.yaml

```yaml
# Environment Configuration
environments:
  dev:
    base_url: "https://dev.example.com"
    api_url: "https://api.dev.example.com"
    username: "test_user"
    password: "test_pass"
  
  staging:
    base_url: "https://staging.example.com"
    api_url: "https://api.staging.example.com"
    username: "staging_user"
    password: "staging_pass"
  
  prod:
    base_url: "https://example.com"
    api_url: "https://api.example.com"
    username: ${PROD_USERNAME}  # Loaded from .env
    password: ${PROD_PASSWORD}  # Loaded from .env

# Playwright Configuration
playwright:
  headless: false          # Run in headless mode
  slow_mo: 100             # Slow down operations by 100ms
  timeout: 30000           # Default timeout 30 seconds
  viewport:
    width: 1920
    height: 1080
  browser: "chromium"      # chromium, firefox, webkit
  trace: "retain-on-failure"  # Capture trace on failure

# Test Configuration
test:
  default_wait_time: 10
  retry_count: 2
  screenshot_on_failure: true
  video_on_failure: true
  max_failures: 5
```

### .env File

```bash
# Production Credentials
PROD_USERNAME=your_prod_username
PROD_PASSWORD=your_prod_password

# Optional: Override any config values
TEST_ENV=staging
BROWSER=firefox
HEADLESS=true
```

## 🏃 Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/ui/test_login.py

# Run specific test function
pytest tests/ui/test_login.py::test_valid_login

# Run tests with specific marker
pytest -m smoke
pytest -m regression
pytest -m api
pytest -m performance

# Run tests with specific environment
pytest --env=staging
pytest --env=prod

# Run tests with specific browser
pytest --browser=firefox
pytest --browser=webkit

# Run tests in headless mode
pytest --headless

# Run tests in parallel (4 workers)
pytest -n 4

# Run tests and generate HTML report
pytest --html=reports/report.html --self-contained-html
```

### Using the Test Runner Script

```bash
# Basic usage
python run_tests.py

# With options
python run_tests.py --env=staging --browser=firefox --headless
python run_tests.py --mark=smoke --workers=4
python run_tests.py --test-path=tests/ui/test_cart.py
python run_tests.py --html-report --allure
```

### Test Markers

| Marker | Description |
|--------|-------------|
| `@pytest.mark.smoke` | Critical path tests |
| `@pytest.mark.regression` | Full regression tests |
| `@pytest.mark.boundary` | Edge case and boundary tests |
| `@pytest.mark.performance` | Performance and load tests |
| `@pytest.mark.api` | API endpoint tests |
| `@pytest.mark.ui` | UI automation tests |
| `@pytest.mark.slow` | Long-running tests |

## 📝 Test Examples

### UI Test Example

```python
import pytest
import allure
from pages.login_page import LoginPage

@pytest.mark.smoke
@allure.feature("Login Functionality")
def test_valid_login(page, config):
    """Test successful login with valid credentials"""
    login_page = LoginPage(page)
    
    login_page.navigate("/login")
    login_page.login(config.username, config.password)
    login_page.verify_login_success()
```

### API Test Example

```python
import pytest
import allure

@pytest.mark.api
@allure.feature("Products API")
def test_get_all_products(api_client):
    """Test retrieving all products"""
    response = api_client.get("/products")
    
    assert response["status_code"] == 200
    assert isinstance(response["data"], list)
```

### Performance Test Example

```python
import pytest
import allure
import time

@pytest.mark.performance
def test_page_load_time(page):
    """Test page load performance"""
    start_time = time.time()
    page.goto("/products")
    end_time = time.time()
    
    load_time = (end_time - start_time) * 1000
    assert load_time < 3000  # Should load within 3 seconds
```

## 📊 Generating Reports

### Allure Report

```bash
# Run tests and generate Allure data
pytest --alluredir=reports/allure-results

# Generate and open Allure report
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### HTML Report

```bash
# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# View in browser
open reports/report.html  # Mac
start reports/report.html # Windows
xdg-open reports/report.html # Linux
```

### Combined Report

```bash
# Generate both reports
pytest --alluredir=reports/allure-results --html=reports/report.html --self-contained-html
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Run Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        playwright install --with-deps ${{ matrix.browser }}
    
    - name: Run tests
      run: |
        pytest --browser=${{ matrix.browser }} \
               --alluredir=reports/allure-results \
               --html=reports/report.html \
               --self-contained-html
    
    - name: Upload Allure results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: allure-results-${{ matrix.browser }}
        path: reports/allure-results
    
    - name: Upload HTML report
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: html-report-${{ matrix.browser }}
        path: reports/report.html
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image: python:3.10

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -r requirements.txt
  - playwright install --with-deps

test:
  parallel:
    matrix:
      - BROWSER: ["chromium", "firefox", "webkit"]
  script:
    - pytest --browser=$BROWSER --alluredir=reports/allure-results --html=reports/report.html
  artifacts:
    when: always
    paths:
      - reports/
    reports:
      junit: reports/junit.xml
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    
    environment {
        PYTHONPATH = "${env.WORKSPACE}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    playwright install
                '''
            }
        }
        
        stage('Run Tests') {
            parallel {
                stage('UI Tests') {
                    steps {
                        sh 'pytest tests/ui/ --alluredir=reports/allure-results'
                    }
                }
                stage('API Tests') {
                    steps {
                        sh 'pytest tests/api/ --alluredir=reports/allure-results'
                    }
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                sh 'allure generate reports/allure-results -o reports/allure-report --clean'
            }
        }
    }
    
    post {
        always {
            publishHTML([
                reportDir: 'reports/allure-report',
                reportFiles: 'index.html',
                reportName: 'Allure Report'
            ])
        }
    }
}
```

## 🛠️ Development

### Code Quality

```bash
# Format code
black .

# Lint code
flake8 tests/ pages/ utils/

# Type checking
mypy tests/ pages/ utils/

# Security checks
bandit -r .
```

### Pre-commit Hooks

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 🤝 Contributing

1. **Fork the repository**

2. **Create your feature branch (git checkout -b feature/amazing-feature)**

3. **Commit your changes (git commit -m 'Add some amazing feature')**

4. **Push to the branch (git push origin feature/amazing-feature)**

5. **Open a Pull Request**

### Development Guidelines

**Follow PEP 8 style guide**

- Write meaningful commit messages

- Add tests for new features

- Update documentation as needed

- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Playwright - Modern web testing framework

- Pytest - Python testing framework

- Allure - Test report framework

- Faker - Test data generation

## 📧 Contact

- Project Maintainer: Sheva Ma

- Email: sheva8.ma@gmail.com

---

⭐ Star this repository if you find it helpful!

