"""
API Client for making HTTP requests
"""
import requests
import json
import allure
from typing import Dict, Any, Optional
from utils.logger import logger

class APIClient:
    """API client for making HTTP requests"""
    
    def __init__(self, base_url: str, timeout: int = 30000):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout / 1000  # Convert to seconds
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        self.auth_token = None
    
    def set_auth_token(self, token: str) -> None:
        """Set authentication token for subsequent requests"""
        self.auth_token = token
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })
    
    def set_headers(self, headers: Dict[str, str]) -> None:
        """Set custom headers"""
        self.session.headers.update(headers)
    
    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform GET request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"GET request to: {url}")
        
        with allure.step(f"GET {endpoint}"):
            if params:
                allure.attach(json.dumps(params, indent=2), name="Request Parameters", 
                            attachment_type=allure.attachment_type.JSON)
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            allure.attach(str(response.status_code), name="Response Status Code",
                        attachment_type=allure.attachment_type.TEXT)
            
            try:
                response_data = response.json()
                allure.attach(json.dumps(response_data, indent=2), name="Response Body",
                            attachment_type=allure.attachment_type.JSON)
            except:
                response_data = response.text
                allure.attach(response_data, name="Response Body",
                            attachment_type=allure.attachment_type.TEXT)
            
            return {
                "status_code": response.status_code,
                "data": response_data,
                "headers": dict(response.headers)
            }
    
    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict] = None, 
             json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform POST request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"POST request to: {url}")
        
        with allure.step(f"POST {endpoint}"):
            if json_data:
                allure.attach(json.dumps(json_data, indent=2), name="Request Body",
                            attachment_type=allure.attachment_type.JSON)
            
            response = self.session.post(url, data=data, json=json_data, timeout=self.timeout)
            
            allure.attach(str(response.status_code), name="Response Status Code",
                        attachment_type=allure.attachment_type.TEXT)
            
            try:
                response_data = response.json()
                allure.attach(json.dumps(response_data, indent=2), name="Response Body",
                            attachment_type=allure.attachment_type.JSON)
            except:
                response_data = response.text
                allure.attach(response_data, name="Response Body",
                            attachment_type=allure.attachment_type.TEXT)
            
            return {
                "status_code": response.status_code,
                "data": response_data,
                "headers": dict(response.headers)
            }
    
    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, data: Optional[Dict] = None,
            json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform PUT request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"PUT request to: {url}")
        
        with allure.step(f"PUT {endpoint}"):
            if json_data:
                allure.attach(json.dumps(json_data, indent=2), name="Request Body",
                            attachment_type=allure.attachment_type.JSON)
            
            response = self.session.put(url, data=data, json=json_data, timeout=self.timeout)
            
            allure.attach(str(response.status_code), name="Response Status Code",
                        attachment_type=allure.attachment_type.TEXT)
            
            try:
                response_data = response.json()
                allure.attach(json.dumps(response_data, indent=2), name="Response Body",
                            attachment_type=allure.attachment_type.JSON)
            except:
                response_data = response.text
            
            return {
                "status_code": response.status_code,
                "data": response_data,
                "headers": dict(response.headers)
            }
    
    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Perform DELETE request"""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"DELETE request to: {url}")
        
        with allure.step(f"DELETE {endpoint}"):
            response = self.session.delete(url, timeout=self.timeout)
            
            allure.attach(str(response.status_code), name="Response Status Code",
                        attachment_type=allure.attachment_type.TEXT)
            
            return {
                "status_code": response.status_code,
                "data": response.text if response.text else {},
                "headers": dict(response.headers)
            }