from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    API_VERSION: str = "/api/v1"
    DB_ADMIN_USER: str
    DB_ADMIN_PASS: str
    DB_NAME: str
    SESSION_EXPIRATION: int


settings = Settings()
