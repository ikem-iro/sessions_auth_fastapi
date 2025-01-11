from motor.motor_asyncio import AsyncIOMotorClient
from utils.settings import settings


client = AsyncIOMotorClient(
    f"mongodb://{settings.DB_ADMIN_USER}:{settings.DB_ADMIN_PASS}@127.0.0.1:27017/"
)
