from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, conint, field_validator


class PostgresSettings(BaseModel):
    user: str = "user"
    password: str = "password"
    db: str = "db_name"
    port: int = 5432

    url: str = "postgresql+asyncpg://user:password@localhost:5432/db_name"

class MongoSettings(BaseModel):
    url:str = "mongodb://localhost:27017/db_name"

class AuthorizationSettings(BaseModel):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: conint(gt=0) = 30

class ElasticsearchSettings(BaseModel):
    hosts: str = "http://elastic:password@localhost:9200"
    timeout: int = 10
    verify_certs: bool = False

    @field_validator("hosts")
    def validate_hosts(cls, value: str) -> list[str]:
        value = value.split(",") if isinstance(value, str) else value
        return value


class RedisSettings(BaseModel):
    host: str = "localhost"
    port: str = 6379

class ProjectSettings(BaseSettings):
    debug: bool = True
    postgres: PostgresSettings = PostgresSettings()
    mongo: MongoSettings = MongoSettings()
    elasticsearch: ElasticsearchSettings = ElasticsearchSettings()
    auth: AuthorizationSettings
    redis: RedisSettings = RedisSettings()
    date_time_format:str = '%Y-%m-%d %H:%M:%S'

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra='ignore',
        env_nested_delimiter="__"
    )


base_settings = ProjectSettings()