import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.integration
class TestUserWorkflow:
    """Integration tests for complete user management workflow."""

    @pytest.fixture
    def api_url(self):
        """Base URL for users API."""
        return f"{settings.api_v1_str}/users"

    async def test_complete_user_lifecycle(self, test_client: AsyncClient, api_url, sample_user_data):
        """Test complete user lifecycle: create, read, update, delete."""
        
        # 1. Create user
        create_response = await test_client.post(api_url + "/", json=sample_user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()
        user_id = created_user["id"]
        
        # 2. Get user by ID
        get_response = await test_client.get(f"{api_url}/{user_id}")
        assert get_response.status_code == 200
        retrieved_user = get_response.json()
        assert retrieved_user["id"] == user_id
        assert retrieved_user["name"] == sample_user_data["name"]
        assert retrieved_user["email"] == sample_user_data["email"]
        
        # 3. Update user
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        update_response = await test_client.put(f"{api_url}/{user_id}", json=update_data)
        assert update_response.status_code == 200
        updated_user = update_response.json()
        assert updated_user["name"] == update_data["name"]
        assert updated_user["email"] == update_data["email"]
        
        # 4. Verify update by getting user again
        get_updated_response = await test_client.get(f"{api_url}/{user_id}")
        assert get_updated_response.status_code == 200
        final_user = get_updated_response.json()
        assert final_user["name"] == update_data["name"]
        assert final_user["email"] == update_data["email"]
        
        # 5. Delete user
        delete_response = await test_client.delete(f"{api_url}/{user_id}")
        assert delete_response.status_code == 204
        
        # 6. Verify deletion
        get_deleted_response = await test_client.get(f"{api_url}/{user_id}")
        assert get_deleted_response.status_code == 404

    async def test_user_list_pagination_workflow(self, test_client: AsyncClient, api_url):
        """Test user list and pagination workflow."""
        
        # Create multiple users
        users_data = [
            {"name": f"User {i}", "email": f"user{i}@example.com"}
            for i in range(15)
        ]
        
        created_users = []
        for user_data in users_data:
            response = await test_client.post(api_url + "/", json=user_data)
            assert response.status_code == 201
            created_users.append(response.json())
        
        # Test getting all users (default pagination)
        list_response = await test_client.get(api_url + "/")
        assert list_response.status_code == 200
        list_data = list_response.json()
        assert list_data["total"] == 15
        assert len(list_data["users"]) == 10  # Default page size
        assert list_data["page"] == 1
        assert list_data["size"] == 10
        
        # Test pagination - page 2
        page2_response = await test_client.get(api_url + "/?page=2&size=10")
        assert page2_response.status_code == 200
        page2_data = page2_response.json()
        assert page2_data["total"] == 15
        assert len(page2_data["users"]) == 5  # Remaining users
        assert page2_data["page"] == 2
        assert page2_data["size"] == 10
        
        # Test custom page size
        custom_size_response = await test_client.get(api_url + "/?page=1&size=5")
        assert custom_size_response.status_code == 200
        custom_size_data = custom_size_response.json()
        assert len(custom_size_data["users"]) == 5
        assert custom_size_data["size"] == 5
        
        # Clean up - delete all created users
        for user in created_users:
            delete_response = await test_client.delete(f"{api_url}/{user['id']}")
            assert delete_response.status_code == 204

    async def test_email_uniqueness_workflow(self, test_client: AsyncClient, api_url):
        """Test email uniqueness constraint workflow."""
        
        user_data = {
            "name": "John Doe",
            "email": "unique@example.com"
        }
        
        # Create first user
        response1 = await test_client.post(api_url + "/", json=user_data)
        assert response1.status_code == 201
        user1 = response1.json()
        
        # Try to create second user with same email
        duplicate_data = {
            "name": "Jane Doe",
            "email": "unique@example.com"  # Same email
        }
        response2 = await test_client.post(api_url + "/", json=duplicate_data)
        assert response2.status_code == 400
        assert "Email already registered" in response2.json()["detail"]
        
        # Create third user with different email
        different_data = {
            "name": "Bob Smith",
            "email": "different@example.com"
        }
        response3 = await test_client.post(api_url + "/", json=different_data)
        assert response3.status_code == 201
        user3 = response3.json()
        
        # Try to update user3's email to user1's email
        update_data = {"email": user1["email"]}
        update_response = await test_client.put(f"{api_url}/{user3['id']}", json=update_data)
        assert update_response.status_code == 400
        assert "Email already registered" in update_response.json()["detail"]
        
        # Update user3's email to a new unique email (should succeed)
        new_email_data = {"email": "newemail@example.com"}
        new_email_response = await test_client.put(f"{api_url}/{user3['id']}", json=new_email_data)
        assert new_email_response.status_code == 200
        assert new_email_response.json()["email"] == "newemail@example.com"
        
        # Clean up
        await test_client.delete(f"{api_url}/{user1['id']}")
        await test_client.delete(f"{api_url}/{user3['id']}")

    async def test_error_handling_workflow(self, test_client: AsyncClient, api_url):
        """Test error handling across different scenarios."""
        
        # Test validation errors
        invalid_data = {
            "name": "",  # Empty name
            "email": "invalid-email"  # Invalid email
        }
        response = await test_client.post(api_url + "/", json=invalid_data)
        assert response.status_code == 422
        
        # Test missing fields
        incomplete_data = {"name": "John Doe"}  # Missing email
        response = await test_client.post(api_url + "/", json=incomplete_data)
        assert response.status_code == 422
        
        # Test operations on non-existent user
        fake_id = "507f1f77bcf86cd799439011"
        
        # Get non-existent user
        get_response = await test_client.get(f"{api_url}/{fake_id}")
        assert get_response.status_code == 404
        
        # Update non-existent user
        update_response = await test_client.put(f"{api_url}/{fake_id}", json={"name": "New Name"})
        assert update_response.status_code == 404
        
        # Delete non-existent user
        delete_response = await test_client.delete(f"{api_url}/{fake_id}")
        assert delete_response.status_code == 404
        
        # Test invalid ID format
        invalid_id = "invalid-id-format"
        
        get_invalid_response = await test_client.get(f"{api_url}/{invalid_id}")
        assert get_invalid_response.status_code == 404
        
        update_invalid_response = await test_client.put(f"{api_url}/{invalid_id}", json={"name": "New Name"})
        assert update_invalid_response.status_code == 404
        
        delete_invalid_response = await test_client.delete(f"{api_url}/{invalid_id}")
        assert delete_invalid_response.status_code == 404
