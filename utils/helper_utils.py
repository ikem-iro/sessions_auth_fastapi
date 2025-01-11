import random
from crud.session_crud import get_expired_sessions, delete_expired_sessions


def individual_serialiser(user) -> dict:
    return {
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "age": user.age,
        "username": user.username,
        "password": user.password,
        "createdAt": user.createdAt,
        "updatedAt": user.updatedAt,
    }


def list_serialiser(users) -> list:
    return [individual_serialiser(user) for user in users]


def generate_otp() -> str:
    return str(random.randint(1000, 9999))


async def remove_expired_sessions():
    # implement logic to remove expired sessions
    expired_session = await get_expired_sessions()
    await delete_expired_sessions(expired_session)
    return True

