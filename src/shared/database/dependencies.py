from fastapi import Depends
from src.shared.database.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

# Alias for easier dependency injection
DatabaseSession = Depends(get_async_session)
