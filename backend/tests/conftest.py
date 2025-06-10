import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from mongomock_motor import AsyncMongoMockClient
from faker import Faker

from app.main import app
from app.core.database import get_database
from app.core.config import settings
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserUpdate


# Configure Faker
fake = Faker()


@pytest.fixture
async def mock_database() -> AsyncIOMotorDatabase:
    """Create a mock MongoDB database for testing."""
    client = AsyncMongoMockClient()
    database = client[f"test_{settings.database_name}"]
    return database


@pytest.fixture
async def test_client(mock_database: AsyncIOMotorDatabase) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with mocked database."""

    async def override_get_database():
        return mock_database

    app.dependency_overrides[get_database] = override_get_database

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data() -> dict:
    """Generate sample user data for testing."""
    return {
        "name": fake.name(),
        "email": fake.email()
    }


@pytest.fixture
def sample_user_create(sample_user_data: dict) -> UserCreate:
    """Create a UserCreate instance with sample data."""
    return UserCreate(**sample_user_data)


@pytest.fixture
def sample_user_update() -> UserUpdate:
    """Create a UserUpdate instance with sample data."""
    return UserUpdate(
        name=fake.name(),
        email=fake.email()
    )


@pytest.fixture
async def created_user(mock_database: AsyncIOMotorDatabase, sample_user_data: dict) -> UserModel:
    """Create a user in the test database and return the UserModel."""
    collection = mock_database.users
    result = await collection.insert_one(sample_user_data)

    created_user_doc = await collection.find_one({"_id": result.inserted_id})
    return UserModel(**created_user_doc)


@pytest.fixture
async def multiple_users(mock_database: AsyncIOMotorDatabase) -> list[UserModel]:
    """Create multiple users in the test database."""
    collection = mock_database.users
    users_data = [
        {"name": fake.name(), "email": fake.email()}
        for _ in range(5)
    ]

    result = await collection.insert_many(users_data)

    users = []
    for inserted_id in result.inserted_ids:
        user_doc = await collection.find_one({"_id": inserted_id})
        users.append(UserModel(**user_doc))

    return users


@pytest.fixture
def invalid_user_data() -> dict:
    """Generate invalid user data for testing validation."""
    return {
        "name": "",  # Invalid: empty name
        "email": "invalid-email"  # Invalid: not a valid email
    }


@pytest.fixture
def user_data_missing_fields() -> dict:
    """Generate user data with missing required fields."""
    return {
        "name": fake.name()
        # Missing email field
    }
