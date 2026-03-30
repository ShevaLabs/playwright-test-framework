"""
API Orders Tests
"""
import pytest
import allure
from utils.api_client import APIClient

@allure.epic("API Testing")
@allure.feature("Orders API")
class TestOrdersAPI:
    
    @allure.story("Get Orders")
    @allure.title("Test get user orders")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_user_orders(self, authenticated_api_client):
        """Test retrieving orders for authenticated user"""
        response = authenticated_api_client.get("/orders")
        
        assert response["status_code"] == 200
        assert isinstance(response["data"], list)
    
    @allure.story("Create Orders")
    @allure.title("Test create new order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order(self, authenticated_api_client):
        """Test creating a new order"""
        order_data = {
            "items": [
                {
                    "product_id": 1,
                    "quantity": 2,
                    "price": 99.99
                }
            ],
            "shipping_address": {
                "address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "country": "USA"
            },
            "payment_method": "credit_card"
        }
        
        response = authenticated_api_client.post("/orders", json_data=order_data)
        
        assert response["status_code"] in [201, 200]
        assert "order_id" in response["data"] or "id" in response["data"]
        assert "status" in response["data"]
    
    @allure.story("Create Orders")
    @allure.title("Test create order with empty cart")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_empty_cart(self, authenticated_api_client):
        """Test creating order with empty cart"""
        order_data = {
            "items": [],
            "shipping_address": {
                "address": "123 Main St",
                "city": "New York",
                "postal_code": "10001",
                "country": "USA"
            }
        }
        
        response = authenticated_api_client.post("/orders", json_data=order_data)
        
        assert response["status_code"] in [400, 422]
        assert "empty" in response["data"].get("message", "").lower()
    
    @allure.story("Update Orders")
    @allure.title("Test update order status")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_order_status(self, authenticated_api_client):
        """Test updating order status"""
        # First create an order
        order_data = {
            "items": [{"product_id": 1, "quantity": 1}],
            "shipping_address": {"address": "Test Address"}
        }
        create_response = authenticated_api_client.post("/orders", json_data=order_data)
        order_id = create_response["data"]["order_id"]
        
        # Update order status
        update_data = {
            "status": "shipped"
        }
        response = authenticated_api_client.put(f"/orders/{order_id}", json_data=update_data)
        
        assert response["status_code"] in [200, 204]
        
        # Verify status update
        get_response = authenticated_api_client.get(f"/orders/{order_id}")
        assert get_response["data"]["status"] == "shipped"
    
    @allure.story("Cancel Orders")
    @allure.title("Test cancel order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_cancel_order(self, authenticated_api_client):
        """Test canceling an order"""
        # First create an order
        order_data = {
            "items": [{"product_id": 1, "quantity": 1}],
            "shipping_address": {"address": "Test Address"}
        }
        create_response = authenticated_api_client.post("/orders", json_data=order_data)
        order_id = create_response["data"]["order_id"]
        
        # Cancel the order
        response = authenticated_api_client.post(f"/orders/{order_id}/cancel")
        
        assert response["status_code"] in [200, 204]
        
        # Verify cancellation
        get_response = authenticated_api_client.get(f"/orders/{order_id}")
        assert get_response["data"]["status"] in ["cancelled", "canceled"]