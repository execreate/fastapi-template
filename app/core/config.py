import os
from enum import Enum
from functools import lru_cache
from typing import Optional, Set

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn


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

    TRUSTED_HOSTS: Set[AnyHttpUrl] = {"app", "localhost", "0.0.0.0"}
    BACKEND_CORS_ORIGINS: Set[AnyHttpUrl] = set()

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False

    DATABASE_URL: Optional[PostgresDsn] = "postgresql://user:pass@localhost:5434/my_db"
    DB_ECHO_LOG: bool = False

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            if self.DATABASE_URL
            else self.DATABASE_URL
        )

    class Config:
        case_sensitive = True


class TestSettings(GlobalSettings):
    DEBUG = True
    ENVIRONMENT = EnvironmentEnum.TEST


class DevelopSettings(GlobalSettings):
    DEBUG = True
    ENVIRONMENT = EnvironmentEnum.DEVELOP


class StagingSettings(GlobalSettings):
    DEBUG = False
    ENVIRONMENT = EnvironmentEnum.STAGING


class ProductionSettings(GlobalSettings):
    DEBUG = False
    ENVIRONMENT = EnvironmentEnum.PRODUCTION


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
