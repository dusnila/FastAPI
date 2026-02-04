from typing import Literal
from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"] 
    LOG_LEVEL: Literal["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"
    

    PRIVATE_KEY_PATH: FilePath

    @property
    def PRIVATE_KEY(self) -> str:
        return self.PRIVATE_KEY_PATH.read_text(encoding="UTF-8")    
    
    PUBLIC_KEY_PATH: FilePath

    @property
    def PUBLIC_KEY(self) -> str:
        return self.PUBLIC_KEY_PATH.read_text(encoding="UTF-8")

    ALGORITHM: str

    TIME_LIVE_REFRESH_TOKEN: int
    TIME_LIVE_ACCESS_TOKEN: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    RABBITMQ_USER: str
    RABBITMQ_PASS: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    model_config = SettingsConfigDict(env_file=".env")

setting = Setting() # type: ignore