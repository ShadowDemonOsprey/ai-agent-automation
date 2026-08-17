"""
Ollama client module.

This module provides communication between the AI agent
and the local Ollama LLM.

The client supports:
- Normal full-response generation
- Streaming token-by-token generation
- Offline fallback when Ollama is not running

It acts as the bridge between the AI agent
and the local Ollama model.
"""


from collections.abc import Iterator

import ollama

from app.core.config import settings
from app.logger import logger


class LocalFallbackModel:
    """
    Deterministic offline response generator.

    Used when Ollama is unreachable so the platform and
    the test suite keep working without a local LLM.
    """


    def generate(self, prompt: str) -> str:
        """
        Produce a helpful offline response.
        """

        request = prompt.strip()

        if "User request:" in request:

            request = request.split(
                "User request:",
                1
            )[1].strip()

        request_preview = (
            request[:80] + "..."
            if len(request) > 80 else request
        )

        return (
            "I am running in offline fallback mode because "
            "the local Ollama model is not connected. "
            f"About your request \"{request_preview}\": "
            "start Ollama to get full language model "
            "answers. Math, statistics, date/time and "
            "knowledge tools work offline."
        )



    def stream(self, prompt: str) -> Iterator[str]:
        """
        Yield the offline response token by token.
        """

        for token in self.generate(prompt).split():

            yield token + " "



class OllamaClient:
    """
    Client wrapper for Ollama.

    Responsible for:
    - Sending prompts to Ollama
    - Receiving complete responses
    - Streaming partial responses
    - Falling back offline when Ollama is unavailable
    """


    def __init__(self):
        """
        Initialize Ollama client.

        Stores:
        - Ollama server configuration
        - Selected LLM model name
        - Offline fallback model
        """

        self.host = settings.ollama_host
        self.model = settings.ollama_model
        self.fallback = LocalFallbackModel()

        self._client = ollama.Client(
            host=self.host,
            timeout=8
        )



    def generate(self, prompt: str) -> str:
        """
        Generate a complete text response using Ollama.

        Falls back to the offline model when the server
        is unreachable.

        Args:
            prompt (str):
                User prompt sent to the LLM.

        Returns:
            str:
                Complete generated response.
        """

        try:

            response = self._client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return (
                response.get("message", {}).get("content", "")
            )

        except Exception as error:

            if not settings.ENABLE_OFFLINE_FALLBACK:
                raise

            logger.warning(
                f"Ollama unavailable ({error}); "
                "using offline fallback model"
            )

            return self.fallback.generate(prompt)



    def stream_generate(self, prompt: str) -> Iterator[str]:
        """
        Generate a streaming response from Ollama.

        Ollama returns small response chunks instead
        of waiting for the entire answer.

        This enables ChatGPT-style token streaming.

        Args:
            prompt (str):
                User prompt sent to the LLM.

        Yields:
            str:
                Individual generated text chunks.

        Connection to AI agent system:
        Agent -> OllamaClient -> Ollama streaming API -> SSE endpoint
        """

        try:

            response_stream = self._client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True
            )

            for chunk in response_stream:

                message = chunk.get("message", {})

                content = message.get("content", "")

                if content:

                    yield content

        except Exception as error:

            if not settings.ENABLE_OFFLINE_FALLBACK:

                yield f"[LLM streaming error: {str(error)}]"

                return

            logger.warning(
                f"Ollama streaming unavailable ({error}); "
                "using offline fallback model"
            )

            yield from self.fallback.stream(prompt)



# Shared Ollama client instance.
# The agent services reuse this single client.
ollama_client = OllamaClient()
