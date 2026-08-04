"""
Application configuration module.

This file loads environment variables and provides
a central place for project settings.

Keeping configuration separate prevents hardcoding
API keys and sensitive information inside the code.
"""

import os
from dotenv import load_dotenv


# Load variables from .env file into the application environment.
load_dotenv()


class Settings:
    """
    Stores application-wide configuration.

    Attributes:
        llm_api_key (str): API key for the language model provider.
        llm_model (str): Name of the LLM model to use.
        app_env (str): Current application environment.
    """

    def __init__(self):
        self.llm_api_key = os.getenv("LLM_API_KEY")
        self.llm_model = os.getenv("LLM_MODEL")
        self.app_env = os.getenv("APP_ENV", "development")


# Create one reusable settings object for the whole application.
settings = Settings()
