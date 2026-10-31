from typing import Optional
from fastapi import Header, HTTPException, status
from app.core.config import settings


async def verify_admin_key(
    x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key"),
    authorization: Optional[str] = Header(None),
) -> bool:
    """
    Security dependency to protect admin endpoints.
    Accepts either 'X-Admin-Key: <key>' or 'Authorization: Bearer <key>'.
    """
    expected_key = settings.ADMIN_API_KEY

    # Check X-Admin-Key header
    if x_admin_key and x_admin_key == expected_key:
        return True

    # Check Authorization Bearer header
    if authorization:
        parts = authorization.split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer" and parts[1] == expected_key:
            return True

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing admin authentication key",
        headers={"WWW-Authenticate": "Bearer"},
    )
