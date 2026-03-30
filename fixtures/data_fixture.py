import pytest
from utils.data_generator import TestDataGenerator
import json
import yaml
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_generator():
    """Test data generator fixture"""
    return TestDataGenerator()

@pytest.fixture
def user_data(test_data_generator):
    """Generate user test data"""
    return test_data_generator.generate_user_data()

@pytest.fixture
def product_data(test_data_generator):
    """Generate product test data"""
    return test_data_generator.generate_product_data()

@pytest.fixture
def boundary_test_cases(test_data_generator):
    """Generate boundary test cases"""
    return test_data_generator.generate_boundary_test_cases()

@pytest.fixture(scope="session")
def test_config_data():
    """Load test data from YAML file"""
    config_path = Path(__file__).parent.parent / "config" / "test_data.yaml"
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

@pytest.fixture(params=["chrome", "firefox", "webkit"])
def browser_type(request):
    """Parameterized browser type for cross-browser testing"""
    return request.param

@pytest.fixture
def api_test_data():
    """API test data"""
    return {
        "get_endpoints": ["/api/users", "/api/products", "/api/orders"],
        "post_endpoints": ["/api/login", "/api/register", "/api/orders"],
        "put_endpoints": ["/api/users/1", "/api/products/1"],
        "delete_endpoints": ["/api/users/1", "/api/orders/1"]
    }