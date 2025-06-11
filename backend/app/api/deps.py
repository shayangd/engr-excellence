from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from ..core.database import get_database
from ..crud.user import UserCRUD


async def get_user_crud(
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> UserCRUD:
    """Dependency to get UserCRUD instance"""
    return UserCRUD(database)
