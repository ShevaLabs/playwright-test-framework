import random
import string
from faker import Faker
from typing import Dict, Any, List

class TestDataGenerator:
    def __init__(self):
        self.fake = Faker()

    def generate_user_data(self) -> Dict[str, Any]:
        """Generate user test data"""
        return {
            "username": self.fake.user_name(),
            "email": self.fake.email(),
            "password": self.generate_password(),
            "first_name": self.fake.first_name(),
            "last_name": self.fake.last_name(),
            "phone": self.fake.phone_number(),
            "address": self.fake.address()
        }

    def generate_product_data(self) -> Dict[str, Any]:
        """Generate product test data"""
        return {
            "name": self.fake.word().capitalize() + " " + self.fake.word(),
            "description": self.fake.text(max_nb_chars=200),
            "price": round(random.uniform(10, 1000), 2),
            "quantity": random.randint(1, 100),
            "category": random.choice(["Electronics", "Clothing", "Books", "Home"]),
            "sku": self.generate_sku()
        }

    def generate_password(self, length: int = 12) -> str:
        """Generate strong password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))

    def generate_sku(self) -> str:
        """Generate SKU"""
        return f"SKU-{random.randint(10000, 99999)}"

    def generate_boundary_test_cases(self) -> List[Dict[str, Any]]:
        """Generate boundary test cases"""
        return [
            # Empty value tests
            {"username": "", "password": "valid", "expected_error": "Username cannot be empty"},
            {"username": "valid", "password": "", "expected_error": "Password cannot be empty"},

            # Length boundary tests
            {"username": "a" * 256, "password": "valid", "expected_error": "Username too long"},
            {"username": "valid", "password": "a" * 5, "expected_error": "Password too short"},
            {"username": "valid", "password": "a" * 129, "expected_error": "Password too long"},

            # Special character tests
            {"username": "user<script>", "password": "valid", "expected_error": "Contains invalid characters"},
            {"username": "user' OR '1'='1", "password": "valid", "expected_error": "Contains invalid characters"},

            # Whitespace handling tests
            {"username": "  user  ", "password": "valid", "should_trim": True},

            # Unicode tests
            {"username": "用户🎯测试", "password": "valid", "should_accept": True},

            # SQL injection tests
            {"username": "' OR '1'='1", "password": "' OR '1'='1", "expected_error": "Login failed"},

            # XSS tests
            {"username": "<script>alert('xss')</script>", "password": "valid", "should_escape": True},
        ]

    def generate_performance_test_data(self, count: int = 100) -> List[Dict[str, Any]]:
        """Generate performance test data"""
        return [self.generate_product_data() for _ in range(count)]

    def generate_invalid_emails(self) -> List[str]:
        """Generate invalid email addresses"""
        return [
            "plainaddress",
            "@missingusername.com",
            "username@.com",
            "username@com",
            "username@domain..com",
            "username@domain.c",
            "username@domain.com.",
            "user name@domain.com",
            "username@domain com",
            "username@@domain.com",
            ".username@domain.com",
            "username.@domain.com",
            "username..name@domain.com",
            "username@-domain.com",
            "username@domain-.com",
        ]

    def generate_valid_emails(self) -> List[str]:
        """Generate valid email addresses"""
        return [
            "test@example.com",
            "test.user@example.com",
            "test-user@example.co.uk",
            "test_user@example-domain.com",
            "test+label@example.com",
            "123456@example.com",
            "test@subdomain.example.com",
        ]