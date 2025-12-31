from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    APP_NAME: str = "AgentCraft-Pro"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"

    DATABASE_URL: str = (
        "postgresql://agentcraft:dev_password@postgres:5432/agentcraft_db"
    )
    REDIS_URL: str = "redis://redis:6379/0"
    VECTOR_DB_URL: str = "http://vectordb:8080"

    OPENAI_API_KEY: Optional[str] = None
    XAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None

    JWT_SECRET: str = "your-secret-key-change-in-production"
    SECRET_KEY: str = "another-secret-key"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost"]

    LANGCHAIN_TEMP: float = 0.7
    LLM_MODEL: str = "grok-beta"
    DEFAULT_LLM_PROVIDER: str = "xai"

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
