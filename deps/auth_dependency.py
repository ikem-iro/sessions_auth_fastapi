from fastapi import Request
from crud.session_crud import get_user_session


async def get_current_user(request: Request):
    session_id = request.cookies.get('session_id')
    user = await get_user_session(session_id)
    return user



