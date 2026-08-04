"""
Test Ollama local LLM connection.

This test verifies:
- Ollama is running.
- TinyLlama model is available.
- Python can communicate with Ollama.
"""


from app.llm.ollama_client import ollama_client


def test_ollama_connection():
    """
    Send a simple prompt to the local model.

    If Ollama works, the model should return text.
    """

    response = ollama_client.generate(
        "Explain artificial intelligence in one sentence."
    )

    # Make sure the model returned something.
    assert response is not None

    # Make sure the response is text.
    assert isinstance(response, str)

    # Make sure the response is not empty.
    assert len(response) > 0