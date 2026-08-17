from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    This class loads environment variables
    and provides default values for the AI Agent system.
    """

    # Application information
    APP_NAME: str = "AI Agent Automation Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Ollama local LLM configuration
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "tinyllama"

    # When True the agent falls back to a deterministic
    # local response generator when Ollama is offline.
    # This keeps the platform usable and tests green
    # without a running LLM server.
    ENABLE_OFFLINE_FALLBACK: bool = True

    # Database connection
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_agent.db"

    # Security
    # When set, all /api/v1 endpoints require this key
    # in the "X-API-Key" header. Empty disables auth.
    API_KEY: Optional[str] = None

    # RAG vector store configuration
    VECTOR_STORE_PATH: str = "data/chroma"
    EMBEDDING_DIMENSION: int = 384
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    RAG_TOP_K: int = 3


    # Pydantic v2 configuration.
    # Loads values from .env file automatically.
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


    # Backward compatibility:
    # Existing project files use lowercase names.
    @property
    def app_name(self):
        return self.APP_NAME


    @property
    def app_env(self):
        return self.APP_ENV


    @property
    def debug(self):
        return self.DEBUG


settings = Settings()