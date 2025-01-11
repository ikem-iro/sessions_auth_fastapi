from schemas.user_db_schema import User, Otp
from utils.pass_utils import hash_password
from utils.helper_utils import generate_otp
from odmantic import ObjectId


async def find_one_user(user, session) -> dict:
    async with session.session() as session:
        if user.email:
            user_in_db = await session.find_one(User, User.email == user.email)
            return user_in_db
        elif user.username:
            user_in_db = await session.find_one(User, User.username == user.username)
            return user_in_db


async def find_user_by_id(user_id, session) -> dict:
    async with session.session() as session:
        user = await session.find_one(User, User.id == ObjectId(user_id))
        return user


async def create_user(user, session) -> dict:
    async with session.session() as session:
        hashed_password = hash_password(user.password)
        new_user = User(**user.model_dump())
        new_user.password = hashed_password
        new_user.first_name = new_user.first_name.lower()
        new_user.last_name = new_user.last_name.lower()
        new_user.username = new_user.username.lower()
        otp = generate_otp()
        hashed_otp = hash_password(otp)
        new_otp = Otp(otp=hashed_otp, user_id=str(new_user.id))
        await session.save(new_user)
        await session.save(new_otp)
        return {"new_user": new_user, "new_otp": otp}
