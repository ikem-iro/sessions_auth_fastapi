from odmantic import Model, Field
from datetime import datetime, timezone


class User(Model):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    age: int = Field(...)
    username: str = Field(...)
    password: str = Field(...)
    createdAt: datetime = Field(default=datetime.now(timezone.utc))
    updatedAt: datetime = Field(default=datetime.now(timezone.utc))


class Otp(Model):
    user_id: str = Field(...)
    otp: str = Field(...)


class Session(Model):
    user_id: str = Field(...)
    session_id: str = Field(...)
    createdAt: datetime = Field(default=datetime.now(timezone.utc))
