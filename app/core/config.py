import os
from enum import Enum
from functools import lru_cache
from typing import Optional, Set

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvironmentEnum(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOP = "develop"
    TEST = "test"


class GlobalSettings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Template"
    API_V1_STR: str = "/v1"

    DOCS_USERNAME: str = "docs_user"
    DOCS_PASSWORD: str = "simple_password"

    TRUSTED_HOSTS: Set[str] = {"app", "localhost", "0.0.0.0", "127.0.0.1"}

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False

    DATABASE_URL: Optional[PostgresDsn] = (
        "postgresql+psycopg://user:pass@localhost:5434/my_db"
    )
    DB_ECHO_LOG: bool = False

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8",
        # E.g. To set a value inside the openai.api_key field,
        # define OPENAI__API_KEY in .env
        env_nested_delimiter="__",
    )


class TestSettings(GlobalSettings):
    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.TEST


class DevelopSettings(GlobalSettings):
    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEVELOP


class StagingSettings(GlobalSettings):
    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.STAGING


class ProductionSettings(GlobalSettings):
    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalSettings:
        match self.environment:
            case EnvironmentEnum.PRODUCTION:
                return ProductionSettings()
            case EnvironmentEnum.STAGING:
                return StagingSettings()
            case EnvironmentEnum.TEST:
                return TestSettings()
            case _:
                return DevelopSettings()


@lru_cache()
def get_configuration() -> GlobalSettings:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
