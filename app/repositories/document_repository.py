"""
Document repository.

Provides synchronous database access to RAG document
metadata. The vector store itself is managed by the
knowledge service.
"""


from sqlalchemy import delete, select

from app.database.session import get_sync_session
from app.models.document import Document


class DocumentRepository:
    """
    Data access for knowledge documents.
    """


    def create(
        self,
        document_id: str,
        filename: str,
        title: str,
        source: str,
        content: str,
        chunk_count: int
    ) -> dict:
        """
        Store document metadata.
        """

        with get_sync_session() as session:

            document = Document(
                document_id=document_id,
                filename=filename,
                title=title,
                source=source,
                chunk_count=chunk_count,
                content=content,
            )

            session.add(document)

            session.commit()

            return self._to_dict(document)



    def get(
        self,
        document_id: str
    ) -> dict | None:
        """
        Return document metadata by public id.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(Document)
                .where(
                    Document.document_id == document_id
                )
            )

            document = result.scalar_one_or_none()

            return (
                self._to_dict(document)
                if document is not None else None
            )



    def list_all(
        self
    ) -> list[dict]:
        """
        Return all stored documents.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(Document)
                .order_by(Document.created_at.desc())
            )

            return [
                self._to_dict(document)
                for document in result.scalars().all()
            ]



    def delete(
        self,
        document_id: str
    ) -> bool:
        """
        Delete document metadata.

        Returns True if a document was removed.
        """

        with get_sync_session() as session:

            result = session.execute(
                delete(Document)
                .where(
                    Document.document_id == document_id
                )
            )

            session.commit()

            return result.rowcount > 0



    def _to_dict(
        self,
        document: Document
    ) -> dict:
        """
        Convert a model row into a plain dictionary.
        """

        return {
            "document_id": document.document_id,
            "filename": document.filename,
            "title": document.title,
            "source": document.source,
            "chunk_count": document.chunk_count,
            "created_at": (
                document.created_at.isoformat()
                if document.created_at else None
            ),
        }



document_repository = DocumentRepository()
