"""
RAG system tests.

Covers:
- Local embeddings (dimension, determinism, similarity)
- Text chunking
- Vector store round trips
- Knowledge service ingestion and search
"""


import numpy as np

import app.rag.service as service_module
from app.rag.chunking import chunk_text
from app.rag.embeddings import embedder
from app.rag.service import knowledge_service
from app.rag.vector_store import VectorStore


def test_embedding_dimension():
    vector = embedder.embed("hello world")
    assert len(vector) == 384


def test_embedding_deterministic():
    assert (
        embedder.embed("hello world")
        == embedder.embed("hello world")
    )


def test_embedding_similarity():
    similar_a = embedder.embed("the cat sat on the mat")
    similar_b = embedder.embed("a cat is sitting on a mat")
    unrelated = embedder.embed("quantum chromodynamics")

    distance_similar = np.linalg.norm(
        np.array(similar_a) - np.array(similar_b)
    )
    distance_unrelated = np.linalg.norm(
        np.array(similar_a) - np.array(unrelated)
    )

    assert distance_similar < distance_unrelated


def test_chunking_single_short_text():
    chunks = chunk_text("Hello world. Short text.")
    assert len(chunks) == 1
    assert "Hello" in chunks[0]


def test_chunking_splits_long_text():
    text = "Sentence one here. Sentence two there. " * 200
    chunks = chunk_text(text, chunk_size=200, overlap=50)
    assert len(chunks) > 1


def test_chunking_handles_empty():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_vector_store_roundtrip(tmp_path):
    store = VectorStore(path=str(tmp_path / "chroma"))

    added = store.add_documents(
        "doc1",
        [
            "The capital of France is Paris.",
            "Quantum computing uses qubits.",
        ],
    )

    assert added == 2
    assert store.count() == 2

    results = store.search(
        "What is the capital of France?",
        top_k=1,
    )

    assert len(results) == 1
    assert "Paris" in results[0]["content"]
    assert 0 <= results[0]["similarity"] <= 1

    store.delete_document("doc1")

    assert store.count() == 0


def test_vector_store_search_empty(tmp_path):
    store = VectorStore(path=str(tmp_path / "chroma"))
    assert store.search("anything") == []


def test_knowledge_service_ingest_and_search(tmp_path, monkeypatch):
    # Isolate the knowledge service to a temp vector store.
    store = VectorStore(path=str(tmp_path / "chroma"))

    monkeypatch.setattr(service_module, "vector_store", store)

    document = knowledge_service.ingest(
        content="The Eiffel Tower is located in Paris, France.",
        filename="travel.txt",
        title="Travel notes",
    )

    assert document["chunk_count"] >= 1

    search = knowledge_service.search(
        "Where is the Eiffel Tower?",
        top_k=1,
    )

    assert search["result_count"] >= 1
    assert "Eiffel" in search["results"][0]["content"]

    assert knowledge_service.get_document(
        document["document_id"]
    ) is not None

    deleted = knowledge_service.delete_document(
        document["document_id"]
    )

    assert deleted is True

    assert knowledge_service.get_document(
        document["document_id"]
    ) is None
