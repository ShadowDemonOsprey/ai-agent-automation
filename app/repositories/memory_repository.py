"""
Long-term memory repository.

Provides synchronous database access to persistent
key-value facts per session.
"""


from sqlalchemy import delete, select

from app.database.session import get_sync_session
from app.models.memory import MemoryRecord
from app.utils.time import utcnow


class MemoryRepository:
    """
    Data access for persistent memory records.
    """


    def set(
        self,
        session_id: str,
        key: str,
        value: str
    ) -> dict:
        """
        Store or update a memory fact.

        If the key already exists for the session,
        its value is updated.

        Returns the stored record as a dictionary.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id,
                    MemoryRecord.key == key
                )
            )

            record = result.scalar_one_or_none()

            if record is None:

                record = MemoryRecord(
                    session_id=session_id,
                    key=key,
                    value=value,
                    updated_at=utcnow()
                )

                session.add(record)

            else:

                record.value = value
                record.updated_at = utcnow()

            session.commit()

            return self._to_dict(record)



    def get(
        self,
        session_id: str,
        key: str
    ) -> dict | None:
        """
        Return a single memory fact.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id,
                    MemoryRecord.key == key
                )
            )

            record = result.scalar_one_or_none()

            return (
                self._to_dict(record)
                if record is not None else None
            )



    def get_all(
        self,
        session_id: str
    ) -> list[dict]:
        """
        Return every memory fact for a session.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id
                )
                .order_by(MemoryRecord.key)
            )

            return [
                self._to_dict(record)
                for record in result.scalars().all()
            ]



    def search(
        self,
        session_id: str,
        query: str
    ) -> list[dict]:
        """
        Search memory facts by keyword match.
        """

        with get_sync_session() as session:

            records = session.execute(
                select(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id
                )
            ).scalars().all()

            keywords = query.lower().split()

            matches = [
                record for record in records
                if any(
                    keyword in (
                        record.key + " " + record.value
                    ).lower()
                    for keyword in keywords
                )
            ]

            return [
                self._to_dict(record)
                for record in matches
            ]



    def delete(
        self,
        session_id: str,
        key: str
    ) -> bool:
        """
        Delete a memory fact.

        Returns True if something was deleted.
        """

        with get_sync_session() as session:

            result = session.execute(
                delete(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id,
                    MemoryRecord.key == key
                )
            )

            session.commit()

            return result.rowcount > 0



    def delete_for_session(
        self,
        session_id: str
    ) -> None:
        """
        Delete all memory for a session.
        """

        with get_sync_session() as session:

            session.execute(
                delete(MemoryRecord)
                .where(
                    MemoryRecord.session_id == session_id
                )
            )

            session.commit()



    def _to_dict(
        self,
        record: MemoryRecord
    ) -> dict:
        """
        Convert a model row into a plain dictionary.
        """

        return {
            "id": record.id,
            "session_id": record.session_id,
            "key": record.key,
            "value": record.value,
            "created_at": (
                record.created_at.isoformat()
                if record.created_at else None
            ),
            "updated_at": (
                record.updated_at.isoformat()
                if record.updated_at else None
            ),
        }



memory_repository = MemoryRepository()
