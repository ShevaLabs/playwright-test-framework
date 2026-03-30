"""
API Products Tests
"""
import pytest
import allure
from utils.api_client import APIClient

@allure.epic("API Testing")
@allure.feature("Products API")
class TestProductsAPI:
    
    @allure.story("Get Products")
    @allure.title("Test get all products")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_all_products(self, api_client):
        """Test retrieving all products"""
        response = api_client.get("/products")
        
        assert response["status_code"] == 200
        assert isinstance(response["data"], list)
        assert len(response["data"]) >= 0
    
    @allure.story("Get Products")
    @allure.title("Test get product by ID")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_product_by_id(self, api_client):
        """Test retrieving a specific product by ID"""
        # First get a product ID
        products_response = api_client.get("/products")
        if products_response["data"]:
            product_id = products_response["data"][0]["id"]
            
            response = api_client.get(f"/products/{product_id}")
            
            assert response["status_code"] == 200
            assert "id" in response["data"]
            assert response["data"]["id"] == product_id
    
    @allure.story("Get Products")
    @allure.title("Test get product with non-existent ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_product_not_found(self, api_client):
        """Test retrieving a product with invalid ID"""
        response = api_client.get("/products/999999")
        
        assert response["status_code"] == 404
        assert "not found" in response["data"].get("message", "").lower()
    
    @allure.story("Create Products")
    @allure.title("Test create new product (authenticated)")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product(self, authenticated_api_client, test_products):
        """Test creating a new product with valid data"""
        product_data = test_products[0]
        
        response = authenticated_api_client.post("/products", json_data=product_data)
        
        assert response["status_code"] in [201, 200]
        assert "id" in response["data"]
        assert response["data"]["name"] == product_data["name"]
        assert response["data"]["price"] == product_data["price"]
    
    @allure.story("Create Products")
    @allure.title("Test create product without authentication")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_product_unauthorized(self, api_client, test_products):
        """Test creating product without auth token"""
        product_data = test_products[0]
        
        response = api_client.post("/products", json_data=product_data)
        
        assert response["status_code"] in [401, 403]
    
    @allure.story("Create Products")
    @allure.title("Test create product with invalid data")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("field,value,expected_error", [
        ("name", "", "Name is required"),
        ("price", -10, "Price must be positive"),
        ("price", "invalid", "Invalid price format"),
        ("quantity", -5, "Quantity cannot be negative"),
    ])
    def test_create_product_invalid_data(self, authenticated_api_client, field, value, expected_error):
        """Test creating product with invalid data"""
        product_data = {
            "name": "Test Product",
            "price": 99.99,
            "quantity": 10
        }
        product_data[field] = value
        
        response = authenticated_api_client.post("/products", json_data=product_data)
        
        assert response["status_code"] in [400, 422]
        assert expected_error.lower() in response["data"].get("message", "").lower()
    
    @allure.story("Update Products")
    @allure.title("Test update product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_update_product(self, authenticated_api_client, test_products):
        """Test updating an existing product"""
        # First create a product
        product_data = test_products[0]
        create_response = authenticated_api_client.post("/products", json_data=product_data)
        product_id = create_response["data"]["id"]
        
        # Update the product
        update_data = {
            "name": "Updated Product Name",
            "price": 149.99
        }
        response = authenticated_api_client.put(f"/products/{product_id}", json_data=update_data)
        
        assert response["status_code"] in [200, 204]
        
        # Verify update
        get_response = authenticated_api_client.get(f"/products/{product_id}")
        assert get_response["data"]["name"] == "Updated Product Name"
        assert get_response["data"]["price"] == 149.99
    
    @allure.story("Delete Products")
    @allure.title("Test delete product")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_product(self, authenticated_api_client, test_products):
        """Test deleting a product"""
        # First create a product
        product_data = test_products[0]
        create_response = authenticated_api_client.post("/products", json_data=product_data)
        product_id = create_response["data"]["id"]
        
        # Delete the product
        response = authenticated_api_client.delete(f"/products/{product_id}")
        
        assert response["status_code"] in [200, 204]
        
        # Verify deletion
        get_response = authenticated_api_client.get(f"/products/{product_id}")
        assert get_response["status_code"] == 404
    
    @allure.story("Search Products")
    @allure.title("Test search products by keyword")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("keyword", ["phone", "watch", "book"])
    def test_search_products(self, api_client, keyword):
        """Test searching products by keyword"""
        response = api_client.get("/products/search", params={"q": keyword})
        
        assert response["status_code"] == 200
        assert isinstance(response["data"], list)
    
    @allure.story("Filter Products")
    @allure.title("Test filter products by category")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("category", ["Electronics", "Clothing", "Books"])
    def test_filter_by_category(self, api_client, category):
        """Test filtering products by category"""
        response = api_client.get("/products", params={"category": category})
        
        assert response["status_code"] == 200
        assert isinstance(response["data"], list)
        
        for product in response["data"]:
            assert product.get("category") == category