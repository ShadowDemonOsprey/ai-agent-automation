"""
Ollama client module.

This module provides communication
between the AI agent and local Ollama LLM.

The client supports:
- Normal full-response generation
- Streaming token-by-token generation

It acts as the bridge between the AI agent
and the local Ollama model.
"""


import ollama

from app.core.config import settings



class OllamaClient:
    """
    Client wrapper for Ollama.

    Responsible for:
    - Sending prompts to Ollama
    - Receiving complete responses
    - Streaming partial responses
    """


    def __init__(self):
        """
        Initialize Ollama client.

        Stores:
        - Ollama server configuration
        - Selected LLM model name
        """

        self.host = settings.ollama_host
        self.model = settings.ollama_model



    def generate(self, prompt: str) -> str:
        """
        Generate a complete text response using Ollama.

        This keeps the original non-streaming behavior
        used by the existing agent pipeline.

        Args:
            prompt (str):
                User prompt sent to the LLM.

        Returns:
            str:
                Complete generated response.
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



    def stream_generate(self, prompt: str):
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
            response_stream = ollama.chat(
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
            """
            Convert Ollama failures into a controlled
            agent-level error message.

            This prevents API crashes and allows
            upper layers to handle failures safely.
            """

            yield f"[LLM streaming error: {str(error)}]"



# Shared Ollama client instance.
# The agent services reuse this single client.
ollama_client = OllamaClient()