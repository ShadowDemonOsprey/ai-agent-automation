"""
Knowledge base API tests.

Covers:
- Document ingestion
- Document listing
- Knowledge search
- Document deletion
"""


from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)



def test_ingest_search_delete_roundtrip():
    """
    Full RAG lifecycle through the API.
    """

    response = client.post(
        "/api/v1/knowledge/documents",
        json={
            "filename": "ml-notes.txt",
            "title": "Machine Learning Notes",
            "content": (
                "Machine learning models learn patterns from data. "
                "Deep learning uses neural networks with many layers "
                "to solve complex tasks."
            ),
        },
    )

    assert response.status_code == 200

    document = response.json()

    assert document["document_id"]
    assert document["chunk_count"] >= 1

    document_id = document["document_id"]

    # List documents.
    list_response = client.get(
        "/api/v1/knowledge/documents"
    )

    assert list_response.status_code == 200

    ids = [
        item["document_id"]
        for item in list_response.json()
    ]

    assert document_id in ids

    # Search the knowledge base.
    search_response = client.post(
        "/api/v1/knowledge/search",
        json={
            "query": "neural networks",
            "top_k": 2,
        },
    )

    assert search_response.status_code == 200

    search = search_response.json()

    assert search["result_count"] >= 1

    # Delete the document.
    delete_response = client.delete(
        f"/api/v1/knowledge/documents/{document_id}"
    )

    assert delete_response.status_code == 200

    # Verify it is gone.
    gone = client.delete(
        f"/api/v1/knowledge/documents/{document_id}"
    )

    assert gone.status_code == 404


def test_ingest_empty_content_rejected():
    response = client.post(
        "/api/v1/knowledge/documents",
        json={"content": "   "},
    )

    assert response.status_code == 422


def test_get_missing_document_404():
    response = client.get(
        "/api/v1/knowledge/documents/nonexistent"
    )

    assert response.status_code == 404
