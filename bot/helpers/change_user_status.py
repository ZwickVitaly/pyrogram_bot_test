from db import async_session, User
from sqlalchemy import update
from settings import logger


async def update_user_status(user_id: int, new_status: str):
    logger.debug(f"Updating user: {user_id} status to '{new_status}'")
    async with async_session() as session:
        async with session.begin():
            await session.execute(update(User).where(User.id == user_id).values(status=new_status))


async def merge_user_status(user_id: int, new_status: str):
    logger.debug(f"Merging user: {user_id} status to '{new_status}'")
    async with async_session() as session:
        async with session.begin():
            user = User(id=user_id, status=new_status)
            await session.merge(user)
            await session.commit()
