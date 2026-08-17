"""
RAG package.

Implements the Retrieval-Augmented Generation pipeline:

Document upload
    |
    v
Text chunking
    |
    v
Local embeddings
    |
    v
ChromaDB vector store
    |
    v
Knowledge retrieval (RAG tool)
"""


from app.rag.chunking import chunk_text
from app.rag.embeddings import LocalEmbedder, embedder
from app.rag.service import knowledge_service
from app.rag.vector_store import vector_store

__all__ = [
    "embedder",
    "LocalEmbedder",
    "chunk_text",
    "vector_store",
    "knowledge_service",
]
