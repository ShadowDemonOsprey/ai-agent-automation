"""
Agent memory module.

This file manages conversation history.

Current version:
- Stores memory in local RAM.
- Keeps messages during the running application.

Future upgrades:
- Save memory to a database.
- Add user-specific memory.
- Add long-term memory retrieval.
"""


class ConversationMemory:
    """
    Stores previous conversation messages.

    The agent will use this history
    to understand previous context.
    """


    def __init__(self):
        """
        Initialize empty conversation history.

        messages stores all user and AI messages.
        """

        self.messages = []


    def add_message(self, role: str, content: str):
        """
        Add a new message to memory.

        Args:
            role (str):
                Who sent the message.
                Example:
                - user
                - assistant

            content (str):
                The actual message text.
        """

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )


    def get_history(self):
        """
        Return all previous messages.

        Returns:
            list:
                Conversation history.
        """

        return self.messages


    def clear(self):
        """
        Delete all stored conversation history.
        """

        self.messages = []


# Create one shared memory instance.
memory = ConversationMemory()