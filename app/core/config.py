"""
Application configuration module.

Loads environment variables and provides
centralized project settings.

All application configuration should come
from this file instead of hardcoding values.
"""


import os
from dotenv import load_dotenv



# Load variables from .env file.
load_dotenv()



class Settings:
    """
    Application settings container.

    Stores:
    - Ollama configuration
    - Application environment
    """


    def __init__(self):
        """
        Initialize application settings.
        """


        # Ollama server address.
        #
        # Example:
        # http://localhost:11434
        self.ollama_host = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )


        # Ollama model name.
        #
        # Example:
        # tinyllama
        self.ollama_model = os.getenv(
            "OLLAMA_MODEL",
            "tinyllama"
        )


        # Current application environment.
        #
        # development / production
        self.app_env = os.getenv(
            "APP_ENV",
            "development"
        )



# Create shared settings object.
#
# Other files import this:
#
# from app.core.config import settings
#
settings = Settings()