from settings import DB_URL, logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

logger.debug(f"Creating engine: {DB_URL}")
engine = create_async_engine(DB_URL)
logger.debug("Creating declarative base")
Base = declarative_base()
logger.debug(f"Creating async session maker. Engine url: {DB_URL}")
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)
