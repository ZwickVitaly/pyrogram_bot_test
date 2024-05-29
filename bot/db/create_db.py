from settings import logger


async def create_db(async_db_engine, db_base):
    logger.debug("Creating db if not exists")
    async with async_db_engine.begin() as conn:
        await conn.run_sync(db_base.metadata.create_all)

