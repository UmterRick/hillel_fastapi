from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class PostgresSettings(BaseModel):
    user: str = "user"
    password: str = "password"
    db: str = "db_name"
    port: int = 5432

    url: str = "postgresql+asyncpg://user:password@host.docker.internal:5432/db_name"
    sync_url: str = "postgresql+psycopg2://admin:admin@localhost:5432/mydb"


class ProjectSettings(BaseSettings):
    debug: bool = True
    postgres: PostgresSettings = PostgresSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )


base_settings = ProjectSettings()
