"""
Test conversation memory.

This verifies:
- Messages can be stored.
- Messages can be retrieved.
- Memory can be cleared.
"""


from app.memory import ConversationMemory


def test_memory_storage():
    """
    Test adding and retrieving messages.
    """

    memory = ConversationMemory()


    # Add a user message.
    memory.add_message(
        "user",
        "Hello AI"
    )


    # Add an assistant message.
    memory.add_message(
        "assistant",
        "Hello! How can I help?"
    )


    history = memory.get_history()


    # Check that two messages were saved.
    assert len(history) == 2


    # Check that the first message is from the user.
    assert history[0]["role"] == "user"


    # Check that the content is correct.
    assert history[0]["content"] == "Hello AI"



def test_memory_clear():
    """
    Test deleting conversation history.
    """

    memory = ConversationMemory()


    memory.add_message(
        "user",
        "Test message"
    )


    memory.clear()


    # After clearing, memory should be empty.
    assert len(memory.get_history()) == 0