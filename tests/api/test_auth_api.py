"""
API Authentication Tests
"""
import pytest
import allure
from utils.api_client import APIClient

@allure.epic("API Testing")
@allure.feature("Authentication API")
class TestAuthAPI:
    
    @allure.story("Login")
    @allure.title("Test successful login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, api_client, config):
        """Test login with valid credentials"""
        login_data = {
            "username": config.username,
            "password": config.password
        }
        
        response = api_client.post("/auth/login", json_data=login_data)
        
        assert response["status_code"] == 200
        assert "token" in response["data"] or "access_token" in response["data"]
        assert "user" in response["data"]
    
    @allure.story("Login")
    @allure.title("Test login failure with invalid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username,password,expected_status", [
        ("invalid_user", "wrong_pass", 401),
        ("", "valid_pass", 400),
        ("valid_user", "", 400),
        ("invalid@user", "pass", 401),
    ])
    def test_login_failure(self, api_client, username, password, expected_status):
        """Test login with invalid credentials"""
        login_data = {
            "username": username,
            "password": password
        }
        
        response = api_client.post("/auth/login", json_data=login_data)
        
        assert response["status_code"] == expected_status
        assert "error" in response["data"] or "message" in response["data"]
    
    @allure.story("Registration")
    @allure.title("Test user registration with valid data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_user(self, api_client, test_data_generator):
        """Test user registration with valid data"""
        user_data = test_data_generator.generate_user_data()
        
        registration_data = {
            "username": user_data["username"],
            "email": user_data["email"],
            "password": user_data["password"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"]
        }
        
        response = api_client.post("/auth/register", json_data=registration_data)
        
        assert response["status_code"] in [201, 200]
        assert "user_id" in response["data"] or "id" in response["data"]
        assert "message" in response["data"]
    
    @allure.story("Registration")
    @allure.title("Test registration with existing username")
    @allure.severity(allure.severity_level.NORMAL)
    def test_register_duplicate_username(self, api_client, config):
        """Test registration with already existing username"""
        registration_data = {
            "username": config.username,
            "email": "newemail@example.com",
            "password": "Test@123456",
            "first_name": "Test",
            "last_name": "User"
        }
        
        response = api_client.post("/auth/register", json_data=registration_data)
        
        assert response["status_code"] in [400, 409]
        assert "exists" in response["data"].get("message", "").lower() or \
               "already" in response["data"].get("message", "").lower()
    
    @allure.story("Logout")
    @allure.title("Test logout functionality")
    @allure.severity(allure.severity_level.NORMAL)
    def test_logout(self, authenticated_api_client):
        """Test logout endpoint"""
        response = authenticated_api_client.post("/auth/logout")
        
        assert response["status_code"] in [200, 204]
    
    @allure.story("Password Reset")
    @allure.title("Test password reset request")
    @allure.severity(allure.severity_level.NORMAL)
    def test_request_password_reset(self, api_client, config):
        """Test requesting password reset"""
        reset_data = {
            "email": config.email
        }
        
        response = api_client.post("/auth/forgot-password", json_data=reset_data)
        
        assert response["status_code"] in [200, 202]
        assert "message" in response["data"]