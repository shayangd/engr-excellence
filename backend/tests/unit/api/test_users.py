import pytest
from httpx import AsyncClient
from bson import ObjectId

from app.core.config import settings


class TestUsersAPI:
    """Test cases for Users API endpoints."""

    @pytest.fixture
    def api_url(self):
        """Base URL for users API."""
        return f"{settings.api_v1_str}/users"

    async def test_create_user_success(self, test_client: AsyncClient, api_url, sample_user_data):
        """Test successful user creation."""
        response = await test_client.post(api_url + "/", json=sample_user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]
        assert "id" in data

    async def test_create_user_invalid_email(self, test_client: AsyncClient, api_url, sample_user_data):
        """Test creating user with invalid email."""
        invalid_data = sample_user_data.copy()
        invalid_data["email"] = "invalid-email"
        
        response = await test_client.post(api_url + "/", json=invalid_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    async def test_create_user_missing_fields(self, test_client: AsyncClient, api_url):
        """Test creating user with missing required fields."""
        incomplete_data = {"name": "John Doe"}  # Missing email
        
        response = await test_client.post(api_url + "/", json=incomplete_data)
        
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    async def test_create_user_empty_name(self, test_client: AsyncClient, api_url, sample_user_data):
        """Test creating user with empty name."""
        invalid_data = sample_user_data.copy()
        invalid_data["name"] = ""
        
        response = await test_client.post(api_url + "/", json=invalid_data)
        
        assert response.status_code == 422

    async def test_create_user_duplicate_email(self, test_client: AsyncClient, api_url, created_user):
        """Test creating user with duplicate email."""
        duplicate_data = {
            "name": "Different Name",
            "email": created_user.email
        }
        
        response = await test_client.post(api_url + "/", json=duplicate_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Email already registered" in data["detail"]

    async def test_get_users_empty_list(self, test_client: AsyncClient, api_url):
        """Test getting users from empty database."""
        response = await test_client.get(api_url + "/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["users"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 10

    async def test_get_users_with_data(self, test_client: AsyncClient, api_url, multiple_users):
        """Test getting users with data in database."""
        response = await test_client.get(api_url + "/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == len(multiple_users)
        assert data["total"] == len(multiple_users)
        assert data["page"] == 1
        assert data["size"] == 10

    async def test_get_users_with_pagination(self, test_client: AsyncClient, api_url, multiple_users):
        """Test getting users with pagination parameters."""
        response = await test_client.get(api_url + "/?page=1&size=3")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) <= 3
        assert data["page"] == 1
        assert data["size"] == 3

    async def test_get_users_invalid_pagination(self, test_client: AsyncClient, api_url):
        """Test getting users with invalid pagination parameters."""
        response = await test_client.get(api_url + "/?page=0&size=-1")
        
        assert response.status_code == 422

    async def test_get_user_by_id_success(self, test_client: AsyncClient, api_url, created_user):
        """Test successful user retrieval by ID."""
        response = await test_client.get(f"{api_url}/{created_user.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_user.id
        assert data["name"] == created_user.name
        assert data["email"] == created_user.email

    async def test_get_user_by_id_not_found(self, test_client: AsyncClient, api_url):
        """Test getting non-existent user by ID."""
        non_existent_id = str(ObjectId())
        response = await test_client.get(f"{api_url}/{non_existent_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"

    async def test_get_user_by_invalid_id(self, test_client: AsyncClient, api_url):
        """Test getting user with invalid ID format."""
        invalid_id = "invalid-id"
        response = await test_client.get(f"{api_url}/{invalid_id}")
        
        assert response.status_code == 404

    async def test_update_user_success(self, test_client: AsyncClient, api_url, created_user):
        """Test successful user update."""
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        response = await test_client.put(f"{api_url}/{created_user.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_user.id
        assert data["name"] == update_data["name"]
        assert data["email"] == update_data["email"]

    async def test_update_user_partial(self, test_client: AsyncClient, api_url, created_user):
        """Test partial user update."""
        update_data = {"name": "Updated Name Only"}
        
        response = await test_client.put(f"{api_url}/{created_user.id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["email"] == created_user.email  # Should remain unchanged

    async def test_update_user_not_found(self, test_client: AsyncClient, api_url):
        """Test updating non-existent user."""
        non_existent_id = str(ObjectId())
        update_data = {"name": "Updated Name"}
        
        response = await test_client.put(f"{api_url}/{non_existent_id}", json=update_data)
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"

    async def test_update_user_invalid_data(self, test_client: AsyncClient, api_url, created_user):
        """Test updating user with invalid data."""
        invalid_data = {"email": "invalid-email"}
        
        response = await test_client.put(f"{api_url}/{created_user.id}", json=invalid_data)
        
        assert response.status_code == 422

    async def test_update_user_duplicate_email(self, test_client: AsyncClient, api_url, multiple_users):
        """Test updating user with duplicate email."""
        user1, user2 = multiple_users[0], multiple_users[1]
        update_data = {"email": user2.email}
        
        response = await test_client.put(f"{api_url}/{user1.id}", json=update_data)
        
        assert response.status_code == 400
        data = response.json()
        assert "Email already registered" in data["detail"]

    async def test_delete_user_success(self, test_client: AsyncClient, api_url, created_user):
        """Test successful user deletion."""
        response = await test_client.delete(f"{api_url}/{created_user.id}")
        
        assert response.status_code == 204
        
        # Verify user is deleted
        get_response = await test_client.get(f"{api_url}/{created_user.id}")
        assert get_response.status_code == 404

    async def test_delete_user_not_found(self, test_client: AsyncClient, api_url):
        """Test deleting non-existent user."""
        non_existent_id = str(ObjectId())
        response = await test_client.delete(f"{api_url}/{non_existent_id}")
        
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "User not found"

    async def test_delete_user_invalid_id(self, test_client: AsyncClient, api_url):
        """Test deleting user with invalid ID format."""
        invalid_id = "invalid-id"
        response = await test_client.delete(f"{api_url}/{invalid_id}")
        
        assert response.status_code == 404
