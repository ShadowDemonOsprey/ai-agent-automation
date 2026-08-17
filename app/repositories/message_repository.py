"""
Message repository.

Provides synchronous database access to conversation
messages. Used by the AI agent (which runs outside the
FastAPI async request cycle) and by session API routes.
"""


from sqlalchemy import delete, select

from app.database.session import get_sync_session
from app.models.message import Message


class MessageRepository:
    """
    Data access for conversation messages.
    """


    def get_messages(
        self,
        session_id: str
    ) -> list[dict]:
        """
        Return all messages for a session,
        ordered by creation time.

        Args:
            session_id:
                Conversation session identifier.

        Returns:
            list of message dictionaries.
        """

        with get_sync_session() as session:

            result = session.execute(
                select(Message)
                .where(
                    Message.session_id == session_id
                )
                .order_by(Message.id)
            )

            return [
                {
                    "id": row.id,
                    "session_id": row.session_id,
                    "role": row.role,
                    "content": row.content,
                    "created_at": (
                        row.created_at.isoformat()
                        if row.created_at else None
                    ),
                }
                for row in result.scalars().all()
            ]



    def add_message(
        self,
        session_id: str,
        role: str,
        content: str
    ) -> None:
        """
        Persist a new message.

        Args:
            session_id:
                Conversation session identifier.
            role:
                Message sender: "user" or "assistant".
            content:
                Message text.
        """

        with get_sync_session() as session:

            message = Message(
                session_id=session_id,
                role=role,
                content=content
            )

            session.add(message)

            session.commit()



    def delete_for_session(
        self,
        session_id: str
    ) -> None:
        """
        Remove every message belonging to a session.

        Used when a conversation session is deleted.
        """

        with get_sync_session() as session:

            session.execute(
                delete(Message)
                .where(
                    Message.session_id == session_id
                )
            )

            session.commit()



    def count(self) -> int:
        """
        Total number of stored messages.
        """

        with get_sync_session() as session:

            return session.query(Message).count()



message_repository = MessageRepository()
