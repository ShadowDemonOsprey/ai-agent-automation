"""
Application configuration module.

Loads environment variables and provides
centralized project settings.

All application configuration should come
from this file instead of hardcoding values.
"""


# ============================================================
# ADDED:
# Literal is used for strict environment validation.
#
# It limits values to a predefined set:
# - development
# - production
# ============================================================

from typing import Literal



# ============================================================
# ADDED:
# Pydantic Settings imports.
#
# BaseSettings:
#   Provides environment variable loading
#   and type validation.
#
# SettingsConfigDict:
#   Configures .env support.
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict



# ============================================================
# CHANGED:
# Replaced the old manual os.getenv() configuration system.
#
# Now:
# - values come from .env automatically
# - values are type checked
# - invalid configuration is detected early
# ============================================================

class Settings(BaseSettings):
    """
    Global application configuration.

    Configuration sources priority:

    1. Environment variables
    2. .env file
    3. Default values below

    This object is imported throughout
    the application.
    """



    # ========================================================
    # ADDED:
    # Application metadata
    # ========================================================

    app_name: str = "AI Agent Automation Platform"



    # ========================================================
    # CHANGED:
    # Environment validation added.
    #
    # Allowed values:
    # - development
    # - production
    #
    # Any other value causes validation failure.
    # ========================================================

    app_env: Literal[
        "development",
        "production"
    ] = "development"



    # ========================================================
    # ADDED:
    # Debug configuration.
    #
    # Used later for:
    # - development logging
    # - API debugging
    # ========================================================

    debug: bool = True



    # ========================================================
    # EXISTING FEATURE PRESERVED:
    # Ollama configuration.
    #
    # Previously loaded with:
    # os.getenv()
    #
    # Now managed by Pydantic.
    # ========================================================

    ollama_host: str = "http://localhost:11434"


    ollama_model: str = "tinyllama"



    # ========================================================
    # ADDED:
    # Pydantic configuration.
    #
    # env_file:
    #   Loads values from .env
    #
    # extra="ignore":
    #   Ignores unrelated environment variables.
    # ========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )



# ============================================================
# Existing public configuration object.
#
# Other files continue using:
#
# from app.core.config import settings
#
# No import changes required.
# ============================================================

settings = Settings()