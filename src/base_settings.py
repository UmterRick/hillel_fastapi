from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, conint


class PostgresSettings(BaseModel):
    user: str = "user"
    password: str = "password"
    db: str = "db_name"
    port: int = 5432

    url: str = "postgresql+asyncpg://user:password@localhost:5432/db_name"


class AuthorizationSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: conint(gt=0) = 30


class ProjectSettings(BaseSettings):
    debug: bool = True
    postgres: PostgresSettings = PostgresSettings()
    auth: AuthorizationSettings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore',
        env_nested_delimiter="__"
    )


base_settings = ProjectSettings()