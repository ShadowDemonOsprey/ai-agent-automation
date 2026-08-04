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

    # Database connection
    DATABASE_URL: str = "sqlite+aiosqlite:///./ai_agent.db"


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