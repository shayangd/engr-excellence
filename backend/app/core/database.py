from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    client: AsyncIOMotorClient = None
    database = None


db = Database()


async def get_database():
    return db.database


async def connect_to_mongo():
    """Create database connection"""
    logger.info("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.database_name]
    logger.info("Connected to MongoDB!")


async def close_mongo_connection():
    """Close database connection"""
    logger.info("Closing connection to MongoDB...")
    db.client.close()
    logger.info("Disconnected from MongoDB!")
