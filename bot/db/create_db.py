from settings import logger
from asyncio import get_event_loop


async def create_db(async_db_engine, db_base):
    logger.debug("Creating db if not exists")
    async with async_db_engine.begin() as conn:
        await conn.run_sync(db_base.metadata.create_all)


def create_db_sync(async_db_engine, db_base):
    get_event_loop().run_until_complete(create_db(async_db_engine, db_base))
