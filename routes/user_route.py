from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from odmantic import AIOEngine
from models.user_models import UserCreate, UserLogin, OtpValidate
from deps.db_dependency import get_db_engine
from deps.auth_dependency import get_current_user
from controllers.user_controller import (
    register_user,
    login_user,
    get_user_data,
    logout_user,
)
from typing import Annotated


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup")
async def register(
    user: UserCreate, session: Annotated[AIOEngine, Depends(get_db_engine)]
) -> dict:
    response = await register_user(user=user, session=session)
    if isinstance(response, HTTPException):
        return JSONResponse(
            status_code=response.status_code,
            content=jsonable_encoder({"error": response.detail}),
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=jsonable_encoder({"data": response}),
    )


@router.post("/signin")
async def login(
    user: UserLogin, session: Annotated[AIOEngine, Depends(get_db_engine)]
) -> dict:
    res = await login_user(user=user, session=session)
    if isinstance(res, HTTPException):
        return JSONResponse(
            status_code=res.status_code,
            content=jsonable_encoder({"error": res.detail}),
        )
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder({"data": res})
    )
    response.set_cookie(
        key="session_id",
        value=res["session_id"],
        httponly=True,
        secure=True,
        expires=datetime.now(tz=timezone.utc) + timedelta(hours=1),
    )
    return response


@router.get("/get-user")
async def get_user(
    session: Annotated[AIOEngine, Depends(get_db_engine)],
    auth_user: Annotated[str, Depends(get_current_user)],
) -> dict:
    response = await get_user_data(session=session, user_session=auth_user)
    if isinstance(response, HTTPException):
        return JSONResponse(
            status_code=response.status_code,
            content=jsonable_encoder({"error": response.detail}),
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder({"data": response})
    )


@router.delete("/logout")
async def logout(
    session: Annotated[AIOEngine, Depends(get_db_engine)],
    auth_user: Annotated[str, Depends(get_current_user)],
):
    res = await logout_user(session=session, user_session=auth_user)
    if isinstance(res, HTTPException):
        return JSONResponse(
            status_code=res.status_code,
            content=jsonable_encoder({"error": res.detail}),
        )

    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=jsonable_encoder({"data": res})
    )

    response.delete_cookie(key="session_id")
    return response


@router.post("/verify-email", deprecated=True)
async def verify_email(
    otp: OtpValidate, session: Annotated[AIOEngine, Depends(get_db_engine)]
):
    pass
