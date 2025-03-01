from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class AuthJWTConfig(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_days: int = 7
    token_type_field: str = "type"


class DataBaseConfig(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str
    provider: str = "postgresql+asyncpg"

    @property
    def dsn(self) -> str:
        return f"{self.provider}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    debug: bool
    base_url: str
    base_dir: Path = BASE_DIR  # ..\fastapi-finance

    db: DataBaseConfig
    cors_origins: list[str]
    run: RunConfig = RunConfig()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()

    model_config = SettingsConfigDict(
        env_file=(base_dir / ".env"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )


def get_settings():
    return Settings()


settings = get_settings()
