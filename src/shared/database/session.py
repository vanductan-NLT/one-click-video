from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.shared.config.settings import settings

# Create async engine
# Note: echo=True will log all SQL queries (good for dev)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

async def get_async_session():
    """Dependency for providing async session to FastAPI routes or application logic"""
    async with async_session_maker() as session:
        yield session
