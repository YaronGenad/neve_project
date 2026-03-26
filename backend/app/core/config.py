from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Redis (optional – required for Sprint 3 caching)
    REDIS_URL: str = Field(default="redis://localhost:6379", env="REDIS_URL")

    # Security
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    # LLM Providers
    LLM_PROVIDER: str = Field(default="gemini", env="LLM_PROVIDER")
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    NVIDIA_API_KEY: str = Field(default="", env="NVIDIA_API_KEY")
    NVIDIA_MODEL: str = Field(default="openai/gpt-oss-20b", env="NVIDIA_MODEL")

    # File Storage
    UPLOAD_DIR: str = Field(default="./uploads", env="UPLOAD_DIR")
    MAX_FILE_SIZE: int = Field(default=10485760, env="MAX_FILE_SIZE")  # 10MB

    # CORS – comma-separated list of allowed origins
    CORS_ORIGINS: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        env="CORS_ORIGINS",
    )

    # Rate limiting (slowapi format: "N/period")
    AUTH_RATE_LIMIT: str = Field(default="10/minute", env="AUTH_RATE_LIMIT")
    GENERATION_RATE_LIMIT: str = Field(default="5/minute", env="GENERATION_RATE_LIMIT")

    # Application
    DEBUG: bool = Field(default=False, env="DEBUG")
    HOST: str = Field(default="0.0.0.0", env="HOST")
    PORT: int = Field(default=8000, env="PORT")

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()