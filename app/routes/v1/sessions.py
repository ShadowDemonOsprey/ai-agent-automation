"""
Conversation session API routes.

Provides:
- Create conversation session
- List conversation sessions
- Retrieve conversation session
- Delete conversation session
- Message history retrieval
- Long-term memory management

Flow:

User
 |
Session API
 |
Database
 |
ConversationSession
 |
AI Agent Memory + Messages
"""


from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_api_key
from app.database.session import get_session
from app.models.request import MemoryRequest
from app.models.session import ConversationSession
from app.repositories.memory_repository import memory_repository
from app.repositories.message_repository import message_repository

router = APIRouter(
    prefix="/api/v1/sessions",
    tags=["Sessions"],
    dependencies=[Depends(require_api_key)],
)



def _serialize_session(session: ConversationSession) -> dict:
    """
    Convert a session row into an API dictionary.
    """

    return {
        "id": session.id,
        "session_id": session.session_id,
        "created_at": (
            session.created_at.isoformat()
            if session.created_at else None
        ),
        "updated_at": (
            session.updated_at.isoformat()
            if session.updated_at else None
        ),
    }



async def _load_session(
    session_id: str,
    db: AsyncSession
) -> ConversationSession:
    """
    Load a session or raise a 404 error.
    """

    result = await db.execute(
        select(ConversationSession)
        .where(
            ConversationSession.session_id == session_id
        )
    )

    session = result.scalar_one_or_none()

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    return session



@router.post("")
async def create_session(
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new conversation session.

    Generates a unique session id
    and stores it in the database.
    """

    session = ConversationSession(
        session_id=str(uuid4())
    )

    db.add(session)

    await db.commit()

    await db.refresh(session)

    return _serialize_session(session)



@router.get("")
async def list_sessions(
    db: AsyncSession = Depends(get_session)
):
    """
    List all conversation sessions.
    """

    result = await db.execute(
        select(ConversationSession)
        .order_by(
            ConversationSession.updated_at.desc()
        )
    )

    sessions = result.scalars().all()

    return [
        _serialize_session(session)
        for session in sessions
    ]



@router.get("/{session_id}")
async def get_session_by_id(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve an existing conversation session.
    """

    session = await _load_session(
        session_id,
        db
    )

    return _serialize_session(session)



@router.delete("/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a conversation session
    and all its data (messages and memory).
    """

    session = await _load_session(
        session_id,
        db
    )

    await db.delete(session)

    await db.commit()

    message_repository.delete_for_session(session_id)

    memory_repository.delete_for_session(session_id)

    return {
        "message": "Session deleted",
        "session_id": session_id,
    }



@router.get("/{session_id}/messages")
async def get_session_messages(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Return the message history of a session.
    """

    await _load_session(
        session_id,
        db
    )

    return message_repository.get_messages(session_id)



@router.post("/{session_id}/memory")
async def set_session_memory(
    session_id: str,
    request: MemoryRequest,
    db: AsyncSession = Depends(get_session)
):
    """
    Store a long-term memory fact for a session.
    """

    await _load_session(
        session_id,
        db
    )

    record = memory_repository.set(
        session_id,
        request.key,
        request.value
    )

    return record



@router.get("/{session_id}/memory")
async def get_session_memory(
    session_id: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Return all long-term memory facts for a session.
    """

    await _load_session(
        session_id,
        db
    )

    return memory_repository.get_all(session_id)



@router.get("/{session_id}/memory/search")
async def search_session_memory(
    session_id: str,
    query: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Search long-term memory by keyword.
    """

    await _load_session(
        session_id,
        db
    )

    return memory_repository.search(session_id, query)



@router.delete("/{session_id}/memory/{key}")
async def delete_session_memory(
    session_id: str,
    key: str,
    db: AsyncSession = Depends(get_session)
):
    """
    Delete one long-term memory fact.
    """

    await _load_session(
        session_id,
        db
    )

    deleted = memory_repository.delete(
        session_id,
        key
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Memory key not found"
        )

    return {
        "message": "Memory deleted",
        "session_id": session_id,
        "key": key,
    }
