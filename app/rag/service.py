"""
Knowledge service.

Coordinates the full RAG pipeline:

Document ingestion:
  text -> chunking -> embeddings -> vector store

Retrieval:
  query -> embeddings -> vector search -> ranked chunks

Also keeps document metadata in the database.
"""


from uuid import uuid4

from app.core.config import settings
from app.logger import logger
from app.rag.chunking import chunk_text
from app.rag.vector_store import vector_store
from app.repositories.document_repository import document_repository


class KnowledgeService:
    """
    High-level RAG operations.
    """


    def ingest(
        self,
        content: str,
        filename: str = "untitled",
        title: str = "",
        source: str = "text"
    ) -> dict:
        """
        Ingest a document into the knowledge base.

        Args:
            content:
                Document text.
            filename:
                Source file name.
            title:
                Optional title.
            source:
                Origin of the document.

        Returns:
            Document metadata dictionary.
        """

        content = (content or "").strip()

        if not content:

            raise ValueError("Document content is empty")

        document_id = str(uuid4())

        chunks = chunk_text(
            content,
            chunk_size=settings.CHUNK_SIZE,
            overlap=settings.CHUNK_OVERLAP,
        )

        chunk_count = vector_store.add_documents(
            document_id,
            chunks,
        )

        document = document_repository.create(
            document_id=document_id,
            filename=filename,
            title=title,
            source=source,
            content=content,
            chunk_count=chunk_count,
        )

        logger.info(
            f"Ingested document {document_id} "
            f"({chunk_count} chunks)"
        )

        return document



    def search(
        self,
        query: str,
        top_k: int | None = None
    ) -> dict:
        """
        Search the knowledge base.

        Returns:
            dict with the query and ranked results.
        """

        results = vector_store.search(
            query,
            top_k=top_k or settings.RAG_TOP_K,
        )

        return {
            "query": query,
            "results": results,
            "result_count": len(results),
        }



    def list_documents(self) -> list[dict]:
        """
        List all ingested documents.
        """

        return document_repository.list_all()



    def get_document(self, document_id: str) -> dict | None:
        """
        Return document metadata.
        """

        return document_repository.get(document_id)



    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document from metadata and vectors.
        """

        vector_store.delete_document(document_id)

        deleted = document_repository.delete(document_id)

        if deleted:

            logger.info(
                f"Deleted document {document_id}"
            )

        return deleted



    def count_chunks(self) -> int:
        """
        Total indexed chunks.
        """

        return vector_store.count()



knowledge_service = KnowledgeService()
