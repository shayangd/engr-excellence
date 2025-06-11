import pytest
from pydantic import ValidationError
from bson import ObjectId

from app.models.user import UserModel, UserUpdate


class TestUserModel:
    """Test cases for UserModel."""

    def test_user_model_creation_with_valid_data(self, sample_user_data):
        """Test creating a UserModel with valid data."""
        user_data = sample_user_data.copy()
        user_data["_id"] = ObjectId()
        
        user = UserModel(**user_data)
        
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert isinstance(user.id, str)

    def test_user_model_creation_with_string_id(self, sample_user_data):
        """Test creating a UserModel with string ID."""
        user_data = sample_user_data.copy()
        user_data["_id"] = str(ObjectId())
        
        user = UserModel(**user_data)
        
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.id == user_data["_id"]

    def test_user_model_creation_with_objectid(self, sample_user_data):
        """Test creating a UserModel with ObjectId."""
        user_data = sample_user_data.copy()
        object_id = ObjectId()
        user_data["_id"] = object_id
        
        user = UserModel(**user_data)
        
        assert user.name == user_data["name"]
        assert user.email == user_data["email"]
        assert user.id == str(object_id)

    def test_user_model_invalid_email(self, sample_user_data):
        """Test UserModel validation with invalid email."""
        user_data = sample_user_data.copy()
        user_data["email"] = "invalid-email"
        user_data["_id"] = ObjectId()
        
        with pytest.raises(ValidationError) as exc_info:
            UserModel(**user_data)
        
        assert "email" in str(exc_info.value)

    def test_user_model_empty_name(self, sample_user_data):
        """Test UserModel validation with empty name."""
        user_data = sample_user_data.copy()
        user_data["name"] = ""
        user_data["_id"] = ObjectId()
        
        with pytest.raises(ValidationError) as exc_info:
            UserModel(**user_data)
        
        assert "name" in str(exc_info.value)

    def test_user_model_name_too_long(self, sample_user_data):
        """Test UserModel validation with name too long."""
        user_data = sample_user_data.copy()
        user_data["name"] = "a" * 101  # Max length is 100
        user_data["_id"] = ObjectId()
        
        with pytest.raises(ValidationError) as exc_info:
            UserModel(**user_data)
        
        assert "name" in str(exc_info.value)

    def test_user_model_missing_required_fields(self):
        """Test UserModel validation with missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            UserModel()
        
        error_str = str(exc_info.value)
        assert "name" in error_str
        assert "email" in error_str

    def test_user_model_json_serialization(self, sample_user_data):
        """Test UserModel JSON serialization."""
        user_data = sample_user_data.copy()
        user_data["_id"] = ObjectId()
        
        user = UserModel(**user_data)
        json_data = user.model_dump()
        
        assert "id" in json_data
        assert json_data["name"] == user_data["name"]
        assert json_data["email"] == user_data["email"]

    def test_user_model_alias_field(self, sample_user_data):
        """Test UserModel with alias field (_id -> id)."""
        user_data = sample_user_data.copy()
        object_id = ObjectId()
        user_data["_id"] = object_id
        
        user = UserModel(**user_data)
        
        # Test that the alias works
        assert user.id == str(object_id)
        
        # Test serialization includes the alias
        json_data = user.model_dump(by_alias=True)
        assert "_id" in json_data


class TestUserUpdate:
    """Test cases for UserUpdate model."""

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

    def test_user_update_name_too_long(self):
        """Test UserUpdate validation with name too long."""
        with pytest.raises(ValidationError) as exc_info:
            UserUpdate(name="a" * 101)  # Max length is 100
        
        assert "name" in str(exc_info.value)

    def test_user_update_dict_excludes_none(self):
        """Test that UserUpdate.dict() excludes None values when needed."""
        user_update = UserUpdate(name="Updated Name")
        
        # Get all fields
        all_data = user_update.model_dump()
        assert "name" in all_data
        assert "email" in all_data
        assert all_data["email"] is None
        
        # Get only non-None fields
        non_none_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        assert "name" in non_none_data
        assert "email" not in non_none_data
