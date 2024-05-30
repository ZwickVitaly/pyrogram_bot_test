from db import User, async_session
from settings import logger
from sqlalchemy import select


async def user_is_alive(user_id):
    logger.debug(f"Checking if user: {user_id} exists and status is 'alive'")
    async with async_session() as session:
        async with session.begin():
            user_q = await session.execute(
                select(User).where(User.id == user_id, User.status == "alive")
            )
            user = user_q.scalar_one_or_none()
    logger.debug(f"User: {user_id} instance: {user}")
    return bool(user)
