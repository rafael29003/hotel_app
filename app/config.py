from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    DSN: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SMTP_USER_FOR_MAIL: str

    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    class Config:
        env_file = ".env"


settings = Settings()
