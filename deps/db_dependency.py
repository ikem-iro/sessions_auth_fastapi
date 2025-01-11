from odmantic import AIOEngine
from config.db_config import client
from utils.settings import settings


async def get_db_engine():
    engine = AIOEngine(client=client, database=settings.DB_NAME)
    return engine
