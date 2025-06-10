from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from typing import List, Optional
from ..models.user import UserModel, UserUpdate
from ..schemas.user import UserCreate
import logging

logger = logging.getLogger(__name__)


class UserCRUD:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.users

    async def create_user(self, user_data: UserCreate) -> UserModel:
        """Create a new user"""
        # Check if email already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("Email already registered")
        
        user_dict = user_data.dict()
        result = await self.collection.insert_one(user_dict)
        
        # Retrieve the created user
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return UserModel(**created_user)

    async def get_user(self, user_id: str) -> Optional[UserModel]:
        """Get user by ID"""
        if not ObjectId.is_valid(user_id):
            return None
        
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return UserModel(**user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Get user by email"""
        user = await self.collection.find_one({"email": email})
        if user:
            return UserModel(**user)
        return None

    async def get_users(self, skip: int = 0, limit: int = 10) -> List[UserModel]:
        """Get list of users with pagination"""
        cursor = self.collection.find().skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        return [UserModel(**user) for user in users]

    async def get_users_count(self) -> int:
        """Get total count of users"""
        return await self.collection.count_documents({})

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[UserModel]:
        """Update user by ID"""
        if not ObjectId.is_valid(user_id):
            return None

        # Remove None values from update data
        update_data = {k: v for k, v in user_data.dict().items() if v is not None}
        
        if not update_data:
            # If no data to update, return current user
            return await self.get_user(user_id)

        # Check if email is being updated and if it already exists
        if "email" in update_data:
            existing_user = await self.collection.find_one({
                "email": update_data["email"],
                "_id": {"$ne": ObjectId(user_id)}
            })
            if existing_user:
                raise ValueError("Email already registered")

        result = await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        
        if result.modified_count:
            return await self.get_user(user_id)
        return None

    async def delete_user(self, user_id: str) -> bool:
        """Delete user by ID"""
        if not ObjectId.is_valid(user_id):
            return False
        
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
