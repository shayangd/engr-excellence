import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse


class TestUserCreate:
    """Test cases for UserCreate schema."""

    def test_user_create_with_valid_data(self, sample_user_data):
        """Test creating UserCreate with valid data."""
        user_create = UserCreate(**sample_user_data)
        
        assert user_create.name == sample_user_data["name"]
        assert user_create.email == sample_user_data["email"]

    def test_user_create_invalid_email(self, sample_user_data):
        """Test UserCreate validation with invalid email."""
        invalid_data = sample_user_data.copy()
        invalid_data["email"] = "invalid-email"
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "email" in str(exc_info.value)

    def test_user_create_empty_name(self, sample_user_data):
        """Test UserCreate validation with empty name."""
        invalid_data = sample_user_data.copy()
        invalid_data["name"] = ""
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "name" in str(exc_info.value)

    def test_user_create_name_too_long(self, sample_user_data):
        """Test UserCreate validation with name too long."""
        invalid_data = sample_user_data.copy()
        invalid_data["name"] = "a" * 101  # Max length is 100
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "name" in str(exc_info.value)

    def test_user_create_missing_fields(self):
        """Test UserCreate validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserCreate()
        
        error_str = str(exc_info.value)
        assert "name" in error_str
        assert "email" in error_str

    def test_user_create_missing_name(self, sample_user_data):
        """Test UserCreate validation with missing name."""
        invalid_data = sample_user_data.copy()
        del invalid_data["name"]
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "name" in str(exc_info.value)

    def test_user_create_missing_email(self, sample_user_data):
        """Test UserCreate validation with missing email."""
        invalid_data = sample_user_data.copy()
        del invalid_data["email"]
        
        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**invalid_data)
        
        assert "email" in str(exc_info.value)


class TestUserUpdate:
    """Test cases for UserUpdate schema."""

    def test_user_update_with_valid_data(self):
        """Test creating UserUpdate with valid data."""
        update_data = {
            "name": "Updated Name",
            "email": "updated@example.com"
        }
        
        user_update = UserUpdate(**update_data)
        
        assert user_update.name == update_data["name"]
        assert user_update.email == update_data["email"]

    def test_user_update_with_partial_data(self):
        """Test creating UserUpdate with partial data."""
        user_update = UserUpdate(name="Updated Name")
        
        assert user_update.name == "Updated Name"
        assert user_update.email is None

    def test_user_update_with_empty_data(self):
        """Test creating UserUpdate with no data."""
        user_update = UserUpdate()
        
        assert user_update.name is None
        assert user_update.email is None

    def test_user_update_invalid_email(self):
        """Test UserUpdate validation with invalid email."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(email="invalid-email")
        
        assert "email" in str(exc_info.value)

    def test_user_update_empty_name(self):
        """Test UserUpdate validation with empty name."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(name="")
        
        assert "name" in str(exc_info.value)


class TestUserResponse:
    """Test cases for UserResponse schema."""

    def test_user_response_with_valid_data(self):
        """Test creating UserResponse with valid data."""
        response_data = {
            "id": "507f1f77bcf86cd799439011",
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        
        user_response = UserResponse(**response_data)
        
        assert user_response.id == response_data["id"]
        assert user_response.name == response_data["name"]
        assert user_response.email == response_data["email"]

    def test_user_response_missing_fields(self):
        """Test UserResponse validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserResponse()
        
        error_str = str(exc_info.value)
        assert "id" in error_str
        assert "name" in error_str
        assert "email" in error_str

    def test_user_response_json_serialization(self):
        """Test UserResponse JSON serialization."""
        response_data = {
            "id": "507f1f77bcf86cd799439011",
            "name": "John Doe",
            "email": "john.doe@example.com"
        }
        
        user_response = UserResponse(**response_data)
        json_data = user_response.model_dump()
        
        assert json_data == response_data


class TestUserListResponse:
    """Test cases for UserListResponse schema."""

    def test_user_list_response_with_valid_data(self):
        """Test creating UserListResponse with valid data."""
        users_data = [
            {
                "id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "email": "john.doe@example.com"
            },
            {
                "id": "507f1f77bcf86cd799439012",
                "name": "Jane Doe",
                "email": "jane.doe@example.com"
            }
        ]
        
        list_data = {
            "users": [UserResponse(**user) for user in users_data],
            "total": 2,
            "page": 1,
            "size": 10
        }
        
        user_list_response = UserListResponse(**list_data)
        
        assert len(user_list_response.users) == 2
        assert user_list_response.total == 2
        assert user_list_response.page == 1
        assert user_list_response.size == 10

    def test_user_list_response_empty_users(self):
        """Test creating UserListResponse with empty users list."""
        list_data = {
            "users": [],
            "total": 0,
            "page": 1,
            "size": 10
        }
        
        user_list_response = UserListResponse(**list_data)
        
        assert len(user_list_response.users) == 0
        assert user_list_response.total == 0
        assert user_list_response.page == 1
        assert user_list_response.size == 10

    def test_user_list_response_missing_fields(self):
        """Test UserListResponse validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserListResponse()
        
        error_str = str(exc_info.value)
        assert "users" in error_str
        assert "total" in error_str
        assert "page" in error_str
        assert "size" in error_str
