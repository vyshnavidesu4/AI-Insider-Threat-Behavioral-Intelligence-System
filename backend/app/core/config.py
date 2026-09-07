import os
from typing import List
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Insider Threat Behavioral Intelligence System"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    # Standard connection string format: postgresql://user:password@host:port/dbname
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/threat_intel_db"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_url(cls, v: str) -> str:
        if isinstance(v, str) and v.startswith("postgres://"):
            # SQLAlchemy 2.0 requires postgresql:// instead of legacy postgres://
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # JWT Authentication
    JWT_SECRET_KEY: str = "regional-bank-soc-insecure-dev-secret-key-change-in-production-93821038"
    JWT_REFRESH_SECRET_KEY: str = "regional-bank-soc-insecure-refresh-dev-secret-key-change-in-production-192837"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7      # 7 days

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"
    )


settings = Settings()
