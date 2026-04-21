from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    api_prefix: str = "/api"
    cors_origins: str = Field(default="http://localhost:3000,http://127.0.0.1:3000")

    database_url: str = "sqlite:///./designgen.db"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    dashscape_api_key: str = ""
    dashscape_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    dashscape_model: str = "qwen-plus"
    dashscape_temperature: float = 0.3
    dashscape_timeout: int = 300

    zip_output_dir: str = "./generated"

    @property
    def cors_origin_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def zip_output_path(self) -> Path:
        return Path(self.zip_output_dir).resolve()


@lru_cache
def get_settings() -> Settings:
    return Settings()
