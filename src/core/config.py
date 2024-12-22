from pathlib import Path

from passlib.context import CryptContext
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    secret_key: str = "123"
    host: str = "localhost"
    port: int = 8000
    debug: bool = False


class AuthConfig(BaseModel):
    model_config = SettingsConfigDict(arbitrary_types_allowed=True)

    pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DatabaseConfig(BaseModel):
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"
    host: str = "localhost"
    port: str = "5432"
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 30
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    def url(self, db_name: str | None = None) -> str:
        db_name = db_name or self.name
        return (
            "postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}/{db_name}"
        )


class RedisConfig(BaseModel):
    HOST: str = "localhost"
    PORT: int = 6379
    DB: int = 3


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{Path(__file__).resolve().parent.parent.parent}/secrets/.env",
        case_sensitive=False,
        env_nested_delimiter="__",
        arbitrary_types_allowed=True,
        env_ignore_empty=True,
        extra="ignore",
    )

    app: AppConfig = AppConfig()
    auth: AuthConfig = AuthConfig()
    db: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()


config = Config()
