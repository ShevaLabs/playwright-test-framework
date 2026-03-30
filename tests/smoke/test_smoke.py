import pytest
import allure
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.smoke
@pytest.mark.regression
@allure.epic("Smoke Tests")
@allure.feature("Critical Functionality")
class TestSmokeTests:
    
    @pytest.fixture(autouse=True)