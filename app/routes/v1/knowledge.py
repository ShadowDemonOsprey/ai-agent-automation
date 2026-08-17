"""
Knowledge base API routes (RAG).

Provides:
- Ingest knowledge documents
- List documents
- Search the knowledge base
- Delete documents

Flow:

Client
  |
Knowledge API
  |
Knowledge Service
  |
Chunking + Embeddings
  |
ChromaDB Vector Store
  |
Retrieval results
"""


from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.core.security import require_api_key
from app.logger import logger
from app.models.request import (
    KnowledgeDocumentRequest,
    KnowledgeSearchRequest,
)
from app.rag.service import knowledge_service

router = APIRouter(
    prefix="/api/v1/knowledge",
    tags=["Knowledge"],
    dependencies=[Depends(require_api_key)],
)



@router.post("/documents")
async def ingest_document(
    request: KnowledgeDocumentRequest
):
    """
    Ingest a document into the knowledge base.

    The document is chunked, embedded and indexed
    for future retrieval.
    """

    try:

        document = knowledge_service.ingest(
            content=request.content,
            filename=request.filename,
            title=request.title,
            source="text",
        )

        logger.info(
            f"Ingested document {document['document_id']}"
        )

        return document

    except ValueError as error:

        raise HTTPException(
            status_code=422,
            detail=str(error)
        )



@router.get("/documents")
async def list_documents():
    """
    List all ingested documents.
    """

    return knowledge_service.list_documents()



@router.get("/documents/{document_id}")
async def get_document(
    document_id: str
):
    """
    Retrieve one document's metadata.
    """

    document = knowledge_service.get_document(document_id)

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document



@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str
):
    """
    Delete a document and its vectors.
    """

    deleted = knowledge_service.delete_document(document_id)

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return {
        "message": "Document deleted",
        "document_id": document_id,
    }



@router.post("/search")
async def search_knowledge(
    request: KnowledgeSearchRequest
):
    """
    Search the knowledge base for relevant chunks.
    """

    return knowledge_service.search(
        request.query,
        top_k=request.top_k,
    )
