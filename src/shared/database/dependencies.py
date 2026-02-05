from typing import Annotated
from fastapi import Depends
from src.shared.database.session import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

# Alias using Annotated for clean and type-safe dependency injection
DatabaseSession = Annotated[AsyncSession, Depends(get_async_session)]
