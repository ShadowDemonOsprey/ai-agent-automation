"""
Agent memory module.

Manages conversation history.

Current capabilities:
- Per-session conversation history
- Persistent storage in the database (Phase 4.3)
- Long-term key-value memory retrieval

The AI agent uses ConversationMemory to remember
previous messages. When a session_id is provided,
history is persisted to the database so it survives
application restarts.
"""


from app.logger import logger
from app.repositories.memory_repository import memory_repository
from app.repositories.message_repository import message_repository


class ConversationMemory:
    """
    Stores conversation messages for one session.
    """


    def __init__(
        self,
        session_id: str | None = None,
        persistent: bool = False
    ):
        """
        Initialize conversation memory.

        Args:
            session_id:
                Optional conversation session. When set
                together with persistent=True, history is
                loaded from and saved to the database.
            persistent:
                When True, messages are stored in the
                database instead of only in RAM.
        """

        self.session_id = session_id
        self.persistent = persistent
        self.messages: list[dict] = []

        if persistent and session_id:

            self.load_history(session_id)



    def load_history(self, session_id: str) -> None:
        """
        Load conversation history from the database.
        """

        self.session_id = session_id

        self.messages = message_repository.get_messages(
            session_id
        )

        logger.info(
            f"Loaded {len(self.messages)} messages "
            f"for session {session_id}"
        )



    def add_message(
        self,
        role: str,
        content: str,
        session_id: str | None = None
    ):
        """
        Add a new message to memory.

        Args:
            role (str):
                Who sent the message.
                Example: "user" or "assistant".
            content (str):
                The actual message text.
            session_id (str | None):
                Override session for persistence.
        """

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

        target = session_id or self.session_id

        if self.persistent and target:

            message_repository.add_message(
                target,
                role,
                content
            )

            self.messages = self.messages[-2:]



    def get_history(self) -> list[dict]:
        """
        Return all previous messages.

        Returns:
            list:
                Conversation history.
        """

        if self.persistent and self.session_id:

            return message_repository.get_messages(
                self.session_id
            )

        return self.messages



    def clear(self) -> None:
        """
        Delete all stored conversation history.
        """

        self.messages = []

        if self.persistent and self.session_id:

            message_repository.delete_for_session(
                self.session_id
            )



    def get_long_term(self) -> list[dict]:
        """
        Return all persistent memory facts for this session.
        """

        if not self.session_id:

            return []

        return memory_repository.get_all(
            self.session_id
        )



# Create one shared default memory instance.
#
# Used by the agent when no session_id is supplied
# (backward-compatible in-RAM behavior).
memory = ConversationMemory()
