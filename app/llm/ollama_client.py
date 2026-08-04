"""
Ollama client module.

This module provides communication
between the AI agent and local Ollama LLM.
"""


import ollama

from app.core.config import settings



class OllamaClient:
    """
    Client wrapper for Ollama.

    Responsible for:
    - Sending prompts
    - Receiving model responses
    """


    def __init__(self):
        """
        Initialize Ollama client.
        """

        self.host = settings.ollama_host
        self.model = settings.ollama_model



    def generate(self, prompt: str) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt (str):
                User prompt sent to LLM.

        Returns:
            str:
                Generated response.
        """


        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        return response["message"]["content"]



# Shared Ollama client instance.
ollama_client = OllamaClient()