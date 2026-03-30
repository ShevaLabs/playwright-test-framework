import pytest
from requests import request
import allure
from playwright.sync_api import Page, BrowserContext
from config.environment import EnvironmentConfig
from utils.logger import setup_logger
from utils.data_generator import TestDataGenerator
from utils.api_client import APIClient

def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Test environment: dev, staging, prod"
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser type: chromium, firefox, webkit"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run in headless mode"
    )
    parser.addoption(
        "--slow-mo",
        action="store",
        default=100,
        type=int,
        help="Operation delay in milliseconds"
    )

@pytest.fixture(scope="session")
def config(request):
    """Global configuration"""
    env = request.config.getoption("--env")
    return EnvironmentConfig(env)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, config):
    """Browser context arguments"""
    playwright_config = config.get_playwright_config()
    return {
        **browser_context_args,
        "viewport": playwright_config.get("viewport"),
        "ignore_https_errors": True,
        "java_script_enabled": True,
    }

@pytest.fixture
def context(browser, config):
    """Browser context"""
    playwright_config = config.get_playwright_config()
    context = browser.new_context(
        viewport=playwright_config.get("viewport"),
        ignore_https_errors=True,
    )

    # Enable tracing
    if playwright_config.get("trace") == "on":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield context

    # Save trace on test failure
    if playwright_config.get("trace") == "retain-on-failure":
        if request.node.rep_call.failed:
            trace_path = f"./traces/{request.node.name}.zip"
            context.tracing.stop(path=trace_path)
        else:
            context.tracing.stop()
    else:
        context.tracing.stop()

    context.close()

@pytest.fixture
def page(context, config):
    """Page fixture"""
    page = context.new_page()

    # Set timeout
    test_config = config.get_test_config()
    page.set_default_timeout(test_config.get("timeout", 30000))

    # Set default navigation timeout
    page.set_default_navigation_timeout(30000)

    yield page

    # Take screenshot on test failure
    if hasattr(page, '_test_failed') and page._test_failed:
        screenshot_path = f"./screenshots/{request.node.name}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        allure.attach.file(screenshot_path, name="failure_screenshot",
                          attachment_type=allure.attachment_type.PNG)

    page.close()

@pytest.fixture
def test_data():
    """Test data fixture"""
    generator = TestDataGenerator()
    return {
        "user": generator.generate_user_data(),
        "product": generator.generate_product_data(),
        "boundary_cases": generator.generate_boundary_test_cases(),
    }

@pytest.fixture(autouse=True)
def setup_logging():
    """Setup logging"""
    logger = setup_logger()
    yield
    # Clean up logs

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Test report hook"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # Mark test as failed
        if "page" in item.fixturenames:
            page = item.funcargs["page"]
            page._test_failed = True

    # Add Allure attachments
    if rep.when == "call":
        if hasattr(item, "funcargs") and "page" in item.funcargs:
            page = item.funcargs["page"]

            # Add page screenshot
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(screenshot, name="screenshot",
                            attachment_type=allure.attachment_type.PNG)
            except:
                pass

            # Add console logs
            if hasattr(page, 'console_log'):
                allure.attach("\n".join(page.console_log), name="console_log",
                            attachment_type=allure.attachment_type.TEXT)

@pytest.fixture(scope="function")
def login_setup(page, config):
    """Login setup fixture"""
    from pages.login_page import LoginPage
    from pages.dashboard_page import DashboardPage

    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    login_page.navigate("/login")
    login_page.login(config.username, config.password)
    dashboard_page.verify_login_success()

    yield dashboard_page

    # Cleanup: logout
    dashboard_page.logout()

@pytest.fixture
def api_client(config) -> APIClient:
    """API client fixture"""
    return APIClient(config.api_url)

@pytest.fixture
def authenticated_api_client(config, api_client) -> APIClient:
    """Authenticated API client fixture"""
    # Perform login to get auth token
    login_data = {
        "username": config.username,
        "password": config.password
    }
    
    response = api_client.post("/auth/login", json_data=login_data)
    
    if response["status_code"] == 200:
        token = response["data"].get("token") or response["data"].get("access_token")
        api_client.set_auth_token(token)
    
    return api_client

@pytest.fixture
def test_products():
    """Test products data fixture"""
    return [
        {
            "name": "API Test Product 1",
            "price": 99.99,
            "description": "Test product created by API",
            "category": "Electronics",
            "quantity": 10
        },
        {
            "name": "API Test Product 2",
            "price": 49.99,
            "description": "Another test product",
            "category": "Books",
            "quantity": 20
        }
    ]