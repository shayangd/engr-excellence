import pytest
from bson import ObjectId

from app.crud.user import UserCRUD
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import UserModel


class TestUserCRUD:
    """Test cases for UserCRUD operations."""

    @pytest.fixture
    async def user_crud(self, mock_database):
        """Create UserCRUD instance with mock database."""
        return UserCRUD(mock_database)

    async def test_create_user_success(self, user_crud, sample_user_create):
        """Test successful user creation."""
        user = await user_crud.create_user(sample_user_create)
        
        assert isinstance(user, UserModel)
        assert user.name == sample_user_create.name
        assert user.email == sample_user_create.email
        assert user.id  # Should have an ID

    async def test_create_user_duplicate_email(self, user_crud, sample_user_create, created_user):
        """Test creating user with duplicate email raises ValueError."""
        # Try to create user with same email as existing user
        duplicate_user_data = UserCreate(
            name="Different Name",
            email=created_user.email
        )
        
        with pytest.raises(ValueError, match="Email already registered"):
            await user_crud.create_user(duplicate_user_data)

    async def test_get_user_success(self, user_crud, created_user):
        """Test successful user retrieval by ID."""
        user = await user_crud.get_user(created_user.id)
        
        assert user is not None
        assert user.id == created_user.id
        assert user.name == created_user.name
        assert user.email == created_user.email

    async def test_get_user_not_found(self, user_crud):
        """Test getting non-existent user returns None."""
        non_existent_id = str(ObjectId())
        user = await user_crud.get_user(non_existent_id)
        
        assert user is None

    async def test_get_user_invalid_id(self, user_crud):
        """Test getting user with invalid ID returns None."""
        invalid_id = "invalid-id"
        user = await user_crud.get_user(invalid_id)
        
        assert user is None

    async def test_get_user_by_email_success(self, user_crud, created_user):
        """Test successful user retrieval by email."""
        user = await user_crud.get_user_by_email(created_user.email)
        
        assert user is not None
        assert user.id == created_user.id
        assert user.email == created_user.email

    async def test_get_user_by_email_not_found(self, user_crud):
        """Test getting user by non-existent email returns None."""
        user = await user_crud.get_user_by_email("nonexistent@example.com")
        
        assert user is None

    async def test_get_users_with_pagination(self, user_crud, multiple_users):
        """Test getting users with pagination."""
        # Get first 3 users
        users = await user_crud.get_users(skip=0, limit=3)
        
        assert len(users) == 3
        assert all(isinstance(user, UserModel) for user in users)

    async def test_get_users_empty_database(self, user_crud):
        """Test getting users from empty database."""
        users = await user_crud.get_users()
        
        assert users == []

    async def test_get_users_count(self, user_crud, multiple_users):
        """Test getting total count of users."""
        count = await user_crud.get_users_count()
        
        assert count == len(multiple_users)

    async def test_get_users_count_empty_database(self, user_crud):
        """Test getting count from empty database."""
        count = await user_crud.get_users_count()
        
        assert count == 0

    async def test_update_user_success(self, user_crud, created_user):
        """Test successful user update."""
        update_data = UserUpdate(
            name="Updated Name",
            email="updated@example.com"
        )
        
        updated_user = await user_crud.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.name == update_data.name
        assert updated_user.email == update_data.email

    async def test_update_user_partial_update(self, user_crud, created_user):
        """Test partial user update (only name)."""
        update_data = UserUpdate(name="Updated Name Only")
        
        updated_user = await user_crud.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.name == update_data.name
        assert updated_user.email == created_user.email  # Should remain unchanged

    async def test_update_user_no_changes(self, user_crud, created_user):
        """Test updating user with no changes."""
        update_data = UserUpdate()  # No fields to update
        
        updated_user = await user_crud.update_user(created_user.id, update_data)
        
        assert updated_user is not None
        assert updated_user.id == created_user.id
        assert updated_user.name == created_user.name
        assert updated_user.email == created_user.email

    async def test_update_user_not_found(self, user_crud):
        """Test updating non-existent user returns None."""
        non_existent_id = str(ObjectId())
        update_data = UserUpdate(name="Updated Name")
        
        updated_user = await user_crud.update_user(non_existent_id, update_data)
        
        assert updated_user is None

    async def test_update_user_invalid_id(self, user_crud):
        """Test updating user with invalid ID returns None."""
        invalid_id = "invalid-id"
        update_data = UserUpdate(name="Updated Name")
        
        updated_user = await user_crud.update_user(invalid_id, update_data)
        
        assert updated_user is None

    async def test_update_user_duplicate_email(self, user_crud, multiple_users):
        """Test updating user with duplicate email raises ValueError."""
        user1, user2 = multiple_users[0], multiple_users[1]
        
        # Try to update user1's email to user2's email
        update_data = UserUpdate(email=user2.email)
        
        with pytest.raises(ValueError, match="Email already registered"):
            await user_crud.update_user(user1.id, update_data)

    async def test_delete_user_success(self, user_crud, created_user):
        """Test successful user deletion."""
        result = await user_crud.delete_user(created_user.id)
        
        assert result is True
        
        # Verify user is deleted
        deleted_user = await user_crud.get_user(created_user.id)
        assert deleted_user is None

    async def test_delete_user_not_found(self, user_crud):
        """Test deleting non-existent user returns False."""
        non_existent_id = str(ObjectId())
        result = await user_crud.delete_user(non_existent_id)
        
        assert result is False

    async def test_delete_user_invalid_id(self, user_crud):
        """Test deleting user with invalid ID returns False."""
        invalid_id = "invalid-id"
        result = await user_crud.delete_user(invalid_id)
        
        assert result is False
