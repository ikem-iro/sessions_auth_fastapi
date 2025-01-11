import re
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserCreate(BaseModel):
    first_name: str = Field(..., example="John")
    last_name: str = Field(..., example="Doe")
    email: EmailStr = Field(...)
    age: int = Field(..., example=18)
    username: str = Field(..., example="johndoe")
    password: str = Field(..., example="Password123!")

    @field_validator("password")
    def validate_password(cls, v):
        password_pattern = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,64}$"
        )

        if not re.match(password_pattern, v):
            raise ValueError(
                "Password must contain at least 8 characters, an uppercase letter, a number and a special character"
            )

        return v

    @field_validator("age")
    def validate_age(cls, v):
        if v < 16:
            raise ValueError("Age must be at least 16")
        return v


class UserLogin(BaseModel):
    username: str | None = Field(default=None, example="johndoe")
    email: str | None = Field(default=None, example="user@example.com")
    password: str = Field(example="Password123!")


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    username: str | None = Field(default=None)
    password: str | None = Field(default=None)

    @field_validator("password")
    def validate_password(cls, v):
        password_pattern = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,64}$"
        )

        if not re.match(password_pattern, v):
            raise ValueError(
                "Password must contain at least 8 characters, an uppercase letter, a number and a special character"
            )

        return v


class OtpValidate(BaseModel):
    otp: str = Field(...)

    @field_validator("otp")
    def validate_otp(cls, v):
        if len(v) != 4 and not v.isdigit():
            raise ValueError("OTP must be 4 digits and must be of type integer")
        return v
