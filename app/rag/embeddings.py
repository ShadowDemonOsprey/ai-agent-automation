"""
Local embedding engine.

Produces deterministic vector embeddings without any
external downloads, so the whole RAG pipeline works
fully offline.

Approach:
- Tokens are extracted as lowercase words plus
  sliding-window bigrams.
- Each token is hashed (MD5) into a fixed-size vector
  with a sign hash for collision spreading.
- Bigrams add a small positional signal.
- Vectors are L2-normalized so cosine similarity
  can be computed with a dot product.

This is intentionally simple and transparent: an
internship-grade local alternative to transformer
models such as all-MiniLM-L6-v2.
"""


import hashlib
import re

import numpy as np


class LocalEmbedder:
    """
    Hash-based local text embedder.
    """


    def __init__(self, dimension: int = 384):
        """
        Args:
            dimension:
                Size of the embedding vectors.
        """

        self.dimension = dimension



    def _tokens(self, text: str) -> list[str]:
        """
        Extract word tokens from text.
        """

        return re.findall(
            r"[a-z0-9]+",
            text.lower()
        )



    def embed(self, text: str) -> list[float]:
        """
        Embed a single text into a normalized vector.

        Args:
            text:
                Text to embed.

        Returns:
            list of floats of length dimension.
        """

        vector = np.zeros(
            self.dimension,
            dtype=np.float64
        )

        tokens = self._tokens(text)

        for index, token in enumerate(tokens):

            self._add_token(vector, token)

            # Bigram positional signal.
            if index < len(tokens) - 1:

                bigram = token + "_" + tokens[index + 1]

                self._add_token(vector, bigram, weight=0.5)

        norm = np.linalg.norm(vector)

        if norm > 0:

            vector = vector / norm

        return vector.tolist()



    def embed_batch(
        self,
        texts: list[str]
    ) -> list[list[float]]:
        """
        Embed multiple texts.
        """

        return [
            self.embed(text)
            for text in texts
        ]



    def _add_token(
        self,
        vector: np.ndarray,
        token: str,
        weight: float = 1.0
    ) -> None:
        """
        Add one token's hash signal to the vector.
        """

        digest = hashlib.md5(
            token.encode("utf-8")
        ).hexdigest()

        index = int(digest, 16) % self.dimension

        # Sign hash spreads collisions across dimensions.
        sign = 1.0 if int(digest[-8:], 16) % 2 == 0 else -1.0

        vector[index] += sign * weight



# Shared embedder instance.
embedder = LocalEmbedder()
