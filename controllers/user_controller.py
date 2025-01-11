from fastapi import status
from fastapi.exceptions import HTTPException
from crud.user_crud import find_one_user, create_user, find_user_by_id
from crud.session_crud import create_session, delete_session
from utils.pass_utils import verify_password
from utils.helper_utils import individual_serialiser


async def register_user(user, session):
    try:
        # check if user exists
        user_exists = await find_one_user(user=user, session=session)
        # raise error if user exists
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="User already exists"
            )
        new_user = await create_user(user=user, session=session)
        formatted_user = individual_serialiser(new_user["new_user"])
        return {"id": formatted_user["id"], "otp": new_user["new_otp"]}
    except HTTPException as e:
        return e


async def login_user(user, session):
    try:
        print(user)
        user_exists = await find_one_user(user=user, session=session)
        print(user_exists)
        if user_exists is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if not verify_password(user.password, user_exists.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        formatted_user = individual_serialiser(user_exists)
        new_session = await create_session(
            user_id=formatted_user["id"], session=session
        )
        return {"id": formatted_user["id"], "session_id": new_session.session_id}

    except HTTPException as e:
        return e


async def get_user_data(session, user_session):
    try:
        # Check if user_session is empty
        if user_session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        user = await find_user_by_id(user_id=user_session.user_id, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unverified user")
        formatted_user = individual_serialiser(user)
        return formatted_user
    except HTTPException as e:
        return e
    

async def logout_user(session, user_session) -> bool:
    try:
        if user_session is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        response = await delete_session(session=session, user_session=user_session)
        if not response:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured")
        return response
    except HTTPException as e:
        return e
