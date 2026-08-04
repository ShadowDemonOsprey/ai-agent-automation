"""
Ollama LLM client module.

This file connects our AI agent to a local Ollama model.

Currently:
- Uses TinyLlama running on your computer.
- No API key is required.
- No internet connection is required after the model is downloaded.

Later:
- We can swap models without changing the agent logic.
"""


import ollama

from app.core.config import settings


class OllamaClient:
    """
    Handles communication with the local Ollama model.
    """

    def __init__(self):
        """
        Initialize the Ollama client.

        The model name comes from configuration.
        """
        self.model = settings.llm_model or "tinyllama"


    def generate(self, prompt: str) -> str:
        """
        Send a prompt to Ollama and return the response.

        Args:
            prompt (str):
                The instruction or question sent to the model.

        Returns:
            str:
                The generated AI response.
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


# Create one shared client instance.
ollama_client = OllamaClient()