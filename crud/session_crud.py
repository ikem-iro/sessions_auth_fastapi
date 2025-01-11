from datetime import datetime, timezone, timedelta
from uuid import uuid4
from schemas.user_db_schema import Session
from utils.settings import settings
from deps.db_dependency import get_db_engine


async def create_session(user_id, session):
    session_id = str(uuid4())
    async with session.session() as session:
        new_session = Session(user_id=user_id, session_id=session_id)
        await session.save(new_session)
        return new_session

async def get_user_session(session_id) -> dict:
    engine = await get_db_engine()
    async with engine.session() as session:
        user_session = await session.find_one(Session, Session.session_id == session_id)
        return user_session



async def delete_session(session, user_session):
    async with session.session() as session:
        await session.delete(user_session)
        return True
        

async def get_expired_sessions() -> list:
    engine = await get_db_engine()
    now = datetime.now(timezone.utc)
    expiration_threshold = now - timedelta(minutes=settings.SESSION_EXPIRATION)
    async with engine.session() as session:
        expired_sessions = await session.find(Session, Session.createdAt < expiration_threshold)
        print(expired_sessions)
        return expired_sessions
    

async def delete_expired_sessions(expired_session):
    engine = await get_db_engine()
    async with engine.session() as session:
        for s in expired_session:
            await session.delete(s)
    