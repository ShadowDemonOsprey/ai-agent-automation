"""
API security module.

Provides optional API key authentication.

When settings.API_KEY is set, every /api/v1 request
must include a matching "X-API-Key" header. When no
key is configured, authentication is disabled and all
requests are allowed (development mode).
"""


from typing import Optional

from fastapi import Header, HTTPException

from app.core.config import settings


def require_api_key(
    x_api_key: Optional[str] = Header(default=None)
) -> str:
    """
    FastAPI dependency enforcing the API key.

    Args:
        x_api_key:
            Value of the X-API-Key header.

    Returns:
        The validated API key.

    Raises:
        HTTPException 401 if the key is missing/invalid.
    """

    if settings.API_KEY and x_api_key != settings.API_KEY:

        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    return x_api_key or ""
