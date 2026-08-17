"""
Vector store.

Persists document chunks and their embeddings using
ChromaDB with a fully local, deterministic embedding
function (no downloads, works offline).
"""


from typing import Any

import chromadb
from chromadb.config import Settings as ChromaSettings

from app.core.config import settings
from app.rag.embeddings import LocalEmbedder


class LocalEmbeddingFunction:
    """
    ChromaDB embedding function backed by LocalEmbedder.

    ChromaDB expects three methods:
    - __call__ for documents
    - embed_query for queries
    - embed_documents for documents
    """


    def __init__(
        self,
        embedder: LocalEmbedder | None = None
    ):
        """
        Args:
            embedder:
                Local embedding engine.
        """

        self._embedder = embedder or LocalEmbedder()

        self._dimension = self._embedder.dimension



    def __call__(self, input: Any):
        """
        Embed a batch of documents.
        """

        return self._embedder.embed_batch(input)



    def embed_documents(self, input: Any):
        """
        Embed a batch of documents.
        """

        return self._embedder.embed_batch(input)



    def embed_query(self, input: Any):
        """
        Embed a batch of queries.
        """

        return self._embedder.embed_batch(input)



    @staticmethod
    def name() -> str:
        """
        Embedding function identifier.
        """

        return "local-hashed-tf"



    def is_legacy(self) -> bool:
        """
        ChromaDB calls this to detect the legacy interface.
        """

        return False



    def get_config(self) -> dict:
        """
        Embedding function configuration persisted by ChromaDB.
        """

        return {
            "dimension": self._dimension,
        }



    def default_space(self) -> str:
        """
        Default distance metric for this embedding function.
        """

        return "l2"



    def supported_spaces(self) -> list[str]:
        """
        Distance metrics supported by this embedding function.
        """

        return ["l2"]



    @classmethod
    def build_from_config(cls, config: dict) -> "LocalEmbeddingFunction":
        """
        Reconstruct the embedding function from persisted config.
        """

        dimension = config.get("dimension", 384)

        return cls(
            embedder=LocalEmbedder(
                dimension=dimension
            )
        )



class VectorStore:
    """
    ChromaDB-backed vector store for knowledge retrieval.
    """


    def __init__(
        self,
        path: str | None = None,
        dimension: int | None = None
    ):
        """
        Args:
            path:
                ChromaDB persistent directory.
            dimension:
                Embedding dimension (must match).
        """

        self.path = path or settings.VECTOR_STORE_PATH

        self.embedder = LocalEmbedder(
            dimension or settings.EMBEDDING_DIMENSION
        )

        self.client = chromadb.PersistentClient(
            path=self.path,
            settings=ChromaSettings(
                anonymized_telemetry=False
            ),
        )

        self.collection = self.client.get_or_create_collection(
            name="knowledge",
            embedding_function=LocalEmbeddingFunction(
                self.embedder
            ),
        )



    def add_documents(
        self,
        document_id: str,
        chunks: list[str],
        metadatas: list[dict] | None = None
    ) -> int:
        """
        Index document chunks.

        Args:
            document_id:
                Public document identifier.
            chunks:
                Chunk texts to embed and store.
            metadatas:
                Optional per-chunk metadata.

        Returns:
            Number of stored chunks.
        """

        if not chunks:
            return 0

        ids = [
            f"{document_id}:{index}"
            for index in range(len(chunks))
        ]

        if metadatas is None:

            metadatas = [
                {
                    "document_id": document_id,
                    "chunk_index": index,
                }
                for index in range(len(chunks))
            ]

        self.collection.add(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
        )

        return len(chunks)



    def search(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:
        """
        Retrieve the most relevant chunks.

        Returns:
            list of results with content, score and metadata.
        """

        if self.collection.count() == 0:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=min(
                top_k,
                self.collection.count()
            ),
        )

        output: list[dict] = []

        ids = results.get("ids", [[]])[0]

        documents = results.get("documents", [[]])[0]

        distances = results.get("distances", [[]])[0]

        metadatas = results.get("metadatas", [[]])[0]

        for index in range(len(ids)):

            # Chroma returns L2 distances; convert to
            # a similarity score in [0, 1].
            distance = distances[index] if index < len(distances) else 0.0

            similarity = max(
                0.0,
                1.0 / (1.0 + distance)
            )

            output.append(
                {
                    "id": ids[index],
                    "content": (
                        documents[index]
                        if index < len(documents) else ""
                    ),
                    "similarity": round(similarity, 4),
                    "metadata": (
                        metadatas[index]
                        if index < len(metadatas) else {}
                    ),
                }
            )

        return output



    def delete_document(
        self,
        document_id: str
    ) -> None:
        """
        Remove every chunk belonging to a document.

        ChromaDB has no partial-id deletion, so chunks
        are matched with the "where" filter.
        """

        where = {"document_id": document_id}

        existing = self.collection.get(where=where)

        ids = existing.get("ids", [])

        if ids:

            self.collection.delete(ids=ids)



    def count(self) -> int:
        """
        Total number of indexed chunks.
        """

        return self.collection.count()



# Shared vector store instance.
vector_store = VectorStore()
